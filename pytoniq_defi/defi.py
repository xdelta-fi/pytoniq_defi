import typing
from enum import Enum

from pytoniq_core import TlbScheme
from pytoniq_core import Cell, Builder, Slice, HashMap, Address
from .payload_type import PayloadType
from types import SimpleNamespace

############################################################
# Jetton
############################################################
"""
transfer#f8a7ea5 query_id:uint64 amount:Coins destination:MsgAddress
           response_destination:MsgAddress custom_payload:(Maybe ^Cell)
           forward_ton_amount:Coins forward_payload:(Either Cell ^Cell)
           = InternalMsgBody;

transfer_notification#7362d09c query_id:uint64 amount:Coins
           sender:MsgAddress forward_payload:(Either Cell ^Cell)
           = InternalMsgBody;

excesses#d53276db query_id:uint64 = InternalMsgBody;

burn#595f07bc query_id:uint64 amount:Coins
       response_destination:MsgAddress custom_payload:(Maybe ^Cell)
       = InternalMsgBody;

// ----- Unspecified by standard, but suggested format of internal message

internal_transfer#178d4519  query_id:uint64 amount:Coins from:MsgAddress
                     response_address:MsgAddress
                     forward_ton_amount:Coins
                     forward_payload:(Either Cell ^Cell)
                     = InternalMsgBody;
burn_notification#7bdd97de query_id:uint64 amount:Coins
       sender:MsgAddress response_destination:MsgAddress
       = InternalMsgBody;
"""

class JettonTransfer(TlbScheme):
    """
    transfer#f8a7ea5 query_id:uint64 amount:Coins destination:MsgAddress
               response_destination:MsgAddress custom_payload:(Maybe ^Cell)
               forward_ton_amount:Coins forward_payload:(Either Cell ^Cell)
               = InternalMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 destination: typing.Optional[Address] = None,
                 response_destination: typing.Optional[Address] = None,
                 custom_payload: typing.Optional[Cell] = None,
                 forward_ton_amount: typing.Optional[int] = 0,
                 forward_payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        if isinstance(destination, str):
            destination = Address(destination)
        if isinstance(response_destination, str):
            response_destination = Address(response_destination)
        self.destination = destination
        self.response_destination = response_destination
        self.custom_payload = custom_payload
        self.forward_ton_amount = forward_ton_amount
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xf8a7ea5, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_address(self.destination) \
            .store_address(self.response_destination)
        builder.store_bit(1).store_ref(self.custom_payload) if self.custom_payload is not None else builder.store_bit(0)
        builder.store_coins(self.forward_ton_amount)
        builder.store_bit(1).store_ref(self.forward_payload) if self.forward_payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice): #
        op = cell_slice.load_uint(32)
        if not op == 0xf8a7ea5:
            raise ValueError(f"Not a JettonTransfer, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   destination=cell_slice.load_address(),
                   response_destination=cell_slice.load_address(),
                   custom_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None,
                   forward_ton_amount=cell_slice.load_coins(),
                   forward_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None)

    op = 0xf8a7ea5
    message_type = PayloadType.internal

class JettonTransferNotification(TlbScheme):
    """
    transfer_notification#7362d09c query_id:uint64 amount:Coins
               sender:MsgAddress forward_payload:(Either Cell ^Cell)
               = InternalMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 sender: typing.Optional[Address] = None,
                 forward_payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        if isinstance(sender, str):
            sender = Address(sender)
        self.sender = sender
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x7362d09c, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_address(self.sender)
        builder.store_bit(1).store_ref(self.forward_payload)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x7362d09c:
            raise ValueError(f"Not a JettonTransferNotification, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   sender=cell_slice.load_address(),
                   forward_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else cell_slice)

    op = 0x7362d09c

    message_type = PayloadType.internal

class JettonExcesses(TlbScheme):
    """
    excesses#d53276db query_id:uint64 = InternalMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0
                 ):
        self.query_id = query_id

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xd53276db, 32) \
            .store_uint(self.query_id, 64)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xd53276db:
            raise ValueError(f"Not a JettonExcesses, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64))

    op = 0xd53276db

    message_type = PayloadType.internal

class JettonBurn(TlbScheme):
    """
    burn#595f07bc query_id:uint64 amount:Coins
           response_destination:MsgAddress custom_payload:(Maybe ^Cell)
           = InternalMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 response_destination: typing.Optional[Address] = None,
                 custom_payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        if isinstance(response_destination, str):
            response_destination = Address(response_destination)
        self.response_destination = response_destination
        self.custom_payload = custom_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x595f07bc, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_address(self.response_destination)
        builder.store_bit(1).store_ref(self.custom_payload) if self.custom_payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x595f07bc:
            raise ValueError(f"Not a JettonBurn, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   response_destination=cell_slice.load_address(),
                   custom_payload=cell_slice.load_ref().begin_parse() if (cell_slice.load_bit() and cell_slice.remaining_refs) else None)
                   # second check is formally incorrect but some jetton_burns have no custom_payload with bit=1

    op = 0x595f07bc

    message_type = PayloadType.internal

class JettonInternalTransfer(TlbScheme):
    """
    internal_transfer#178d4519  query_id:uint64 amount:Coins from:MsgAddress
                     response_address:MsgAddress
                     forward_ton_amount:Coins
                     forward_payload:(Either Cell ^Cell)
                     = InternalMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 from_: typing.Optional[Address] = None,
                 response_address: typing.Optional[Address] = None,
                 forward_ton_amount: typing.Optional[int] = 0,
                 forward_payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        if isinstance(from_, str):
            from_ = Address(from_)
        if isinstance(response_address, str):
            response_address = Address(response_address)
        self.from_ = from_
        self.response_address = response_address
        self.forward_ton_amount = forward_ton_amount
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x178d4519, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_address(self.from_) \
            .store_address(self.response_address) \
            .store_coins(self.forward_ton_amount)
        builder.store_bit(1).store_ref(self.forward_payload)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x178d4519:
            raise ValueError(f"Not a JettonInternalTransfer, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   from_=cell_slice.load_address(),
                   response_address=cell_slice.load_address(),
                   forward_ton_amount=cell_slice.load_coins(),
                   forward_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else cell_slice)

    op = 0x178d4519

    message_type = PayloadType.internal


class JettonBurnNotification(TlbScheme):
    """
    burn_notification#7bdd97de query_id:uint64 amount:Coins
           sender:MsgAddress response_destination:MsgAddress
           = InternalMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 sender: typing.Optional[Address] = None,
                 response_destination: typing.Optional[Address] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        if isinstance(sender, str):
            sender = Address(sender)
        if isinstance(response_destination, str):
            response_destination = Address(response_destination)
        self.sender = sender
        self.response_destination = response_destination

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x7bdd97de, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_address(self.sender) \
            .store_address(self.response_destination)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x7bdd97de:
            raise ValueError(f"Not a JettonBurnNotification, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   sender=cell_slice.load_address(),
                   response_destination=cell_slice.load_address())

    op = 0x7bdd97de

    message_type = PayloadType.internal


class JettonComment(TlbScheme):
    """

    """
    def __init__(self, comment:typing.Optional[str]):
        self.comment = comment

    def serialize(self) -> Cell:
        builder = Builder()
        builder.store_uint(0x0, 32)
        builder.store_snake_string(self.comment)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x0:
            raise ValueError(f"Not a JettonComment, unknown operation: {op}")
        return cls(comment=cell_slice.load_snake_string())

    op = 0x0

    message_type = PayloadType.jetton


############################################################
# Dedust v2 https://docs.dedust.io/reference/tlb-schemes
############################################################

class DedustSwapParams(TlbScheme):
    """
    timestamp#_ _:uint32 = Timestamp;
    swap_params#_ deadline:Timestamp recipient_addr:MsgAddressInt referral_addr:MsgAddress
              fulfill_payload:(Maybe ^Cell) reject_payload:(Maybe ^Cell) = SwapParams;
    """
    def __init__(self,
                 deadline: typing.Optional[int] = 0,
                 recipient_addr: typing.Optional[Address] = None,
                 referral_addr: typing.Optional[Address] = None,
                 fulfill_payload: typing.Optional[Cell] = None,
                 reject_payload: typing.Optional[Cell] = None
                 ):
        self.deadline = deadline
        if isinstance(recipient_addr, str):
            recipient_addr = Address(recipient_addr)
        if isinstance(referral_addr, str):
            referral_addr = Address(referral_addr)
        self.recipient_addr = recipient_addr
        self.referral_addr = referral_addr
        self.fulfill_payload = fulfill_payload
        self.reject_payload = reject_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(self.deadline, 32) \
            .store_address(self.recipient_addr) \
            .store_address(self.referral_addr)
        builder.store_bit(1).store_ref(self.fulfill_payload) if self.fulfill_payload is not None else builder.store_bit(0)
        builder.store_bit(1).store_ref(self.reject_payload) if self.reject_payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        return cls(deadline         = cell_slice.load_uint(32),
                   recipient_addr   = cell_slice.load_address(),
                   referral_addr    = cell_slice.load_address(),
                   fulfill_payload  = cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None,
                   reject_payload   = cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None)


class DedustSwapStep(TlbScheme):
    """
    given_in$0 = SwapKind;
    given_out$1 = SwapKind;

    step_params#_ kind:SwapKind limit:Coins next:(Maybe ^SwapStep) = SwapStepParams;

    step#_ pool_addr:MsgAddressInt params:SwapStepParams = SwapStep;
    """
    def __init__(self,
                 pool_addr: typing.Optional[Address] = None,
                 step_params = None # DedustSwapStepParams, but we can't annotate it here due to circular imports
                 ):
        if isinstance(pool_addr, str):
            pool_addr = Address(pool_addr)
        self.pool_addr = pool_addr
        self.step_params = step_params

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_address(self.pool_addr) \
            .store_cell(self.step_params.serialize())
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        return cls(pool_addr=cell_slice.load_address(), step_params=DedustSwapStepParams.deserialize(cell_slice))

class SwapKind(Enum):
    """
        given_in$0 = SwapKind;
        given_out$1 = SwapKind;
    """
    given_in = 0
    given_out = 1

    def serialize(self) -> Cell:
        builder = Builder()
        builder.store_uint(self.value, 1)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        return cls(cell_slice.load_uint(1))


class DedustSwapStepParams(TlbScheme):
    """
        given_in$0 = SwapKind;
        given_out$1 = SwapKind;

        step_params#_ kind:SwapKind limit:Coins next:(Maybe ^SwapStep) = SwapStepParams;

        step#_ pool_addr:MsgAddressInt params:SwapStepParams = SwapStep;
    """
    def __init__(self,
                 kind: typing.Optional[SwapKind] = 0,
                 limit: typing.Optional[int] = 0,
                 next: typing.Optional[DedustSwapStep] = None
                 ):
        self.kind = kind
        self.limit = limit
        self.next = next

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_cell(self.kind.serialize()) \
            .store_coins(self.limit)
        builder.store_bit(1).store_ref(self.next.serialize()) if self.next is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        return cls(kind=SwapKind.deserialize(cell_slice),
                   limit=cell_slice.load_coins(),
                   next=DedustSwapStep.deserialize(cell_slice.load_ref().begin_parse()) if cell_slice.load_bit() else None)

class DedustMessageSwap(TlbScheme):
    """
        swap#ea06185d query_id:uint64 amount:Coins _:SwapStep swap_params:^SwapParams = InMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 step: typing.Optional[DedustSwapStep] = None,
                 swap_params: typing.Optional[DedustSwapParams] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        self.step = step
        self.swap_params = swap_params

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xea06185d, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_cell(self.step.serialize()) \
            .store_ref(self.swap_params.serialize())
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xea06185d:
          raise ValueError(f"Not a DedustMessageSwap, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   step=DedustSwapStep.deserialize(cell_slice),
                   swap_params=DedustSwapParams.deserialize(cell_slice.load_ref().begin_parse()))


class DedustPoolType(Enum):
    """
        volatile$0 = PoolType;
        stable$1 = PoolType;
    """
    volatile = 0
    stable = 1

    def serialize(self) -> Cell:
        builder = Builder()
        builder.store_uint(self.value, 1)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        return cls(cell_slice.load_uint(1))

class DedustAsset(TlbScheme):
    """
        native$0000 = Asset;
        jetton$0001 workchain_id:int8 address:uint256 = Asset;
        extra_currency$0010 currency_id:int32 = Asset;
    """

    def __init__(self, type= None, workchain_id = None, address = None, currency_id = None):
        if type == None:
            if not ((workchain_id == None) and (address == None)):
                self.type = 1
            elif currency_id:
                self.type = 2
            else:
                raise ValueError("Undetermined DedustAsset: type, (workchain_id, address) or currency_id should be provided")
        elif type == 1:
            if (workchain_id == None) or (address == None):
                raise ValueError("DedustAsset type 1 should have workchain_id and address")
        elif type == 2:
            if currency_id == None:
                raise ValueError("DedustAsset type 2 should have currency_id")

        self.type = type
        self.workchain_id = workchain_id
        self.address = address
        self.currency_id = currency_id


    def serialize(self) -> Cell:
        builder = Builder()
        if type == 0:
            builder.store_uint(0, 4)
        elif type == 1:
            builder.store_uint(1, 4)
            builder.store_int(self.workchain_id, 8)
            builder.store_uint(self.address, 256)
        elif type == 2:
            builder.store_uint(2, 4)
            builder.store_int(self.currency_id, 32)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        type = cell_slice.load_uint(4)
        if type == 0:
            return cls(type = 0)
        elif type == 1:
            return cls(type = 1, workchain_id = cell_slice.load_int(8), address = cell_slice.load_uint(256))
        elif type == 2:
            return cls(type = 2, currency_id = cell_slice.load_int(32))
        else:
            raise ValueError(f"Not a DedustAsset, unknown type: {type}")
    

class DedustPoolParams(TlbScheme):
    """
        pool_params#_ pool_type:PoolType asset0:Asset asset1:Asset = PoolParams;
    """
    def __init__(self,
                 pool_type: typing.Optional[DedustPoolType] = 0,
                 asset0: typing.Optional[DedustAsset] = 0,
                 asset1: typing.Optional[DedustAsset] = 0
                 ):
        self.pool_type = pool_type
        self.asset0 = asset0
        self.asset1 = asset1

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_cell(self.pool_type.serialize()) \
            .store_cell(self.asset0.serialize()) \
            .store_cell(self.asset1.serialize())
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        return cls(pool_type=DedustPoolType.deserialize(cell_slice),
                   asset0=DedustAsset.deserialize(cell_slice),
                   asset1=DedustAsset.deserialize(cell_slice))

class DedustMessageSwap(TlbScheme):
    """
        swap#ea06185d query_id:uint64 amount:Coins _:SwapStep swap_params:^SwapParams = InMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 step: typing.Optional[DedustSwapStep] = None,
                 swap_params: typing.Optional[DedustSwapParams] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        self.step = step
        self.swap_params = swap_params

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xea06185d, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_cell(self.step.serialize()) \
            .store_ref(self.swap_params.serialize())
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xea06185d:
            raise ValueError(f"Not a DedustMessageSwap, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   step=DedustSwapStep.deserialize(cell_slice),
                   swap_params=DedustSwapParams.deserialize(cell_slice.load_ref().begin_parse()))

    op = 0xea06185d

    message_type = PayloadType.internal


#Message "deposit_liquidity"
class DedustMessageDepositLiquidity(TlbScheme):
    """
        deposit_liquidity#d55e4686 query_id:uint64 amount:Coins pool_params:PoolParams
                                   min_lp_amount:Coins
                                   asset0_target_balance:Coins asset1_target_balance:Coins
                                   fulfill_payload:(Maybe ^Cell)
                                   reject_payload:(Maybe ^Cell) = InMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 amount: typing.Optional[int] = 0,
                 pool_params: typing.Optional[DedustPoolParams] = None,
                 min_lp_amount: typing.Optional[int] = 0,
                 asset0_target_balance: typing.Optional[int] = 0,
                 asset1_target_balance: typing.Optional[int] = 0,
                 fulfill_payload: typing.Optional[Cell] = None,
                 reject_payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.amount = amount
        self.pool_params = pool_params
        self.min_lp_amount = min_lp_amount
        self.asset0_target_balance = asset0_target_balance
        self.asset1_target_balance = asset1_target_balance
        self.fulfill_payload = fulfill_payload
        self.reject_payload = reject_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xd55e4686, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.amount) \
            .store_cell(self.pool_params.serialize()) \
            .store_coins(self.min_lp_amount) \
            .store_coins(self.asset0_target_balance) \
            .store_coins(self.asset1_target_balance)
        builder.store_bit(1).store_ref(self.fulfill_payload) if self.fulfill_payload is not None else builder.store_bit(0)
        builder.store_bit(1).store_ref(self.reject_payload) if self.reject_payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xd55e4686:
          raise ValueError(f"Not a DedustMessageDepositLiquidity, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   amount=cell_slice.load_coins(),
                   pool_params=DedustPoolParams.deserialize(cell_slice),
                   min_lp_amount=cell_slice.load_coins(),
                   asset0_target_balance=cell_slice.load_coins(),
                   asset1_target_balance=cell_slice.load_coins(),
                   fulfill_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None,
                   reject_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None)

    op = 0xd55e4686

    message_type = PayloadType.internal

class DedustMessagePayoutFromPool(TlbScheme):
    """
        pay_out_from_pool#ad4eb6f5 query_id:uint64 proof:^Cell amount:(VarUInteger 16) recipient_addr:MsgAddress payload:(Maybe ^Cell) = InMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 proof: typing.Optional[Cell] = None,
                 amount: typing.Optional[int] = 0,
                 recipient_addr: typing.Optional[Address] = None,
                 payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.proof = proof
        self.amount = amount
        if isinstance(recipient_addr, str):
            recipient_addr = Address(recipient_addr)
        self.recipient_addr = recipient_addr
        self.payload = payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xad4eb6f5, 32) \
            .store_uint(self.query_id, 64) \
            .store_ref(self.proof) \
            .store_coins(self.amount) \
            .store_address(self.recipient_addr)
        builder.store_bit(1).store_ref(self.payload) if self.payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xad4eb6f5:
          raise ValueError(f"Not a DedustMessagePayoutFromPool, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   proof=cell_slice.load_ref().begin_parse(),
                   amount=cell_slice.load_coins(),
                   recipient_addr=cell_slice.load_address(),
                   payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None)

    op = 0xad4eb6f5

    message_type = PayloadType.internal


# Message payout

class DedustMessagePayout(TlbScheme):
    """
        payout#474f86cf query_id:uint64 payload:(Maybe ^Cell) = InMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.payload = payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x474f86cf, 32) \
            .store_uint(self.query_id, 64)
        builder.store_bit(1).store_ref(self.payload) if self.payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x474f86cf:
          raise ValueError(f"Not a DedustMessagePayout, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None)

    op = 0x474f86cf

    message_type = PayloadType.internal

# Message JettonPayloadSwap

class DedustJettonPayloadSwap(TlbScheme):
    """
    swap#e3a0d482 _:SwapStep swap_params:^SwapParams = ForwardPayload;
    """
    def __init__(self,
                 step: typing.Optional[DedustSwapStep] = None,
                 swap_params: typing.Optional[DedustSwapParams] = None
                 ):
        self.step = step
        self.swap_params = swap_params

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xe3a0d482, 32) \
            .store_cell(self.step.serialize()) \
            .store_ref(self.swap_params.serialize())
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xe3a0d482:
          raise ValueError(f"Not a DedustJettonPayloadSwap, unknown operation: {op}")
        return cls(step=DedustSwapStep.deserialize(cell_slice),
                   swap_params=DedustSwapParams.deserialize(cell_slice.load_ref().begin_parse()))

    op = 0xe3a0d482

    message_type = PayloadType.jetton

# Message JettonPayloadDepositLiquidity

class DedustJettonPayloadDepositLiquidity(TlbScheme):
    """
        deposit_liquidity#40e108d6 pool_params:PoolParams min_lp_amount:Coins
                               asset0_target_balance:Coins asset1_target_balance:Coins
                               fulfill_payload:(Maybe ^Cell)
                               reject_payload:(Maybe ^Cell) = ForwardPayload;
    """

    def __init__(self,
                 pool_params: typing.Optional[DedustPoolParams] = None,
                 min_lp_amount: typing.Optional[int] = 0,
                 asset0_target_balance: typing.Optional[int] = 0,
                 asset1_target_balance: typing.Optional[int] = 0,
                 fulfill_payload: typing.Optional[Cell] = None,
                 reject_payload: typing.Optional[Cell] = None
                 ):
        self.pool_params = pool_params
        self.min_lp_amount = min_lp_amount
        self.asset0_target_balance = asset0_target_balance
        self.asset1_target_balance = asset1_target_balance
        self.fulfill_payload = fulfill_payload
        self.reject_payload = reject_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x40e108d6, 32) \
            .store_cell(self.pool_params.serialize()) \
            .store_coins(self.min_lp_amount) \
            .store_coins(self.asset0_target_balance) \
            .store_coins(self.asset1_target_balance)
        builder.store_bit(1).store_ref(self.fulfill_payload) if self.fulfill_payload is not None else builder.store_bit(0)
        builder.store_bit(1).store_ref(self.reject_payload) if self.reject_payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x40e108d6:
          raise ValueError(f"Not a DedustJettonPayloadDepositLiquidity, unknown operation: {op}")
        return cls(pool_params=DedustPoolParams.deserialize(cell_slice),
                   min_lp_amount=cell_slice.load_coins(),
                   asset0_target_balance=cell_slice.load_coins(),
                   asset1_target_balance=cell_slice.load_coins(),
                   fulfill_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None,
                   reject_payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None)

    op = 0x40e108d6

    message_type = PayloadType.jetton

# Message cancel_deposit

class DedustMessageCancelDeposit(TlbScheme):
    """
    cancel_deposit#166cedee query_id:uint64 payload:(Maybe ^Cell) = InMsgBody;
    """
    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 payload: typing.Optional[Cell] = None
                 ):
        self.query_id = query_id
        self.payload = payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x166cedee, 32) \
            .store_uint(self.query_id, 64)
        builder.store_bit(1).store_ref(self.payload) if self.payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x166cedee:
          raise ValueError(f"Not a DedustMessageCancelDeposit, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   payload=cell_slice.load_ref().begin_parse() if cell_slice.load_bit() else None)

    op = 0x166cedee

    message_type = PayloadType.internal

############################################################
# Ston.fi v1
############################################################
"""
swap#25938561 token_wallet:MsgAddress min_out:Coins to_address:MsgAddress referral_address:(Maybe MsgAddress) = JettonPayload;
provide_liquidity#fcf9e58f token_wallet:MsgAddress min_lp_out:Coins = JettonPayload;
swap_success#c64370e5 = JettonPayload;
swap_success_referal#45078540 = JettonPayload;
swap_error_no_liquidity#5ffe1295 = JettonPayload;
swap_error_reserve_error#38976e9b = JettonPayload;
"""
class StonfiMessageSwap(TlbScheme):
    """
    swap#25938561 token_wallet:MsgAddress min_out:Coins to_address:MsgAddress referral_address:(Maybe MsgAddress) = JettonPayload;
    """
    def __init__(self,
                 token_wallet: typing.Optional[Address] = None,
                 min_out: typing.Optional[int] = 0,
                 to_address: typing.Optional[Address] = None,
                 referral_address: typing.Optional[Address] = None
                 ):
        if isinstance(token_wallet, str):
            token_wallet = Address(token_wallet)
        if isinstance(to_address, str):
            to_address = Address(to_address)
        if isinstance(referral_address, str):
            referral_address = Address(referral_address)
        self.token_wallet = token_wallet
        self.min_out = min_out
        self.to_address = to_address
        self.referral_address = referral_address

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x25938561, 32) \
            .store_address(self.token_wallet) \
            .store_coins(self.min_out) \
            .store_address(self.to_address)
        builder.store_bit(1).store_address(self.referral_address) if self.referral_address is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x25938561:
          raise ValueError(f"Not a StonSwap, unknown operation: {op}")
        return cls(token_wallet=cell_slice.load_address(),
                   min_out=cell_slice.load_coins(),
                   to_address=cell_slice.load_address(),
                   referral_address=cell_slice.load_address() if cell_slice.load_bit() else None)

    op = 0x25938561

    message_type = PayloadType.jetton

class StonfiMessageProvideLiquidity(TlbScheme):
    """
    provide_liquidity#fcf9e58f token_wallet:MsgAddress min_lp_out:Coins = JettonPayload;
    """
    def __init__(self,
                 token_wallet: typing.Optional[Address] = None,
                 min_lp_out: typing.Optional[int] = 0
                 ):
        if isinstance(token_wallet, str):
            token_wallet = Address(token_wallet)
        self.token_wallet = token_wallet
        self.min_lp_out = min_lp_out

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0xfcf9e58f, 32) \
            .store_address(self.token_wallet) \
            .store_coins(self.min_lp_out)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xfcf9e58f:
          raise ValueError(f"Not a StonProvideLiquidity, unknown operation: {op}")
        return cls(token_wallet=cell_slice.load_address(),
                   min_lp_out=cell_slice.load_coins())

    op = 0xfcf9e58f

    message_type = PayloadType.jetton

class StonfiMessageSwapSuccess(TlbScheme):
    """
    swap_success#c64370e5 = JettonPayload;
    """
    def __init__(self):
        pass

    def serialize(self) -> Cell:
        builder = Builder()
        builder.store_uint(0xc64370e5, 32)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0xc64370e5:
          raise ValueError(f"Not a StonSwapSuccess, unknown operation: {op}")
        return cls()

    op = 0xc64370e5

    message_type = PayloadType.jetton

class StonfiMessageSwapSuccessReferal(TlbScheme):
    """
    swap_success_referal#45078540 = JettonPayload;
    """
    def __init__(self):
        pass

    def serialize(self) -> Cell:
        builder = Builder()
        builder.store_uint(0x45078540, 32)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x45078540:
          raise ValueError(f"Not a StonSwapSuccessReferal, unknown operation: {op}")
        return cls()

    op = 0x45078540

    message_type = PayloadType.jetton

class StonfiMessageSwapErrorNoLiquidity(TlbScheme):
    """
    swap_error_no_liquidity#5ffe1295 = JettonPayload;
    """
    def __init__(self):
        pass

    def serialize(self) -> Cell:
        builder = Builder()
        builder.store_uint(0x5ffe1295, 32)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x5ffe1295:
          raise ValueError(f"Not a StonSwapErrorNoLiquidity, unknown operation: {op}")
        return cls()

    op = 0x5ffe1295

    message_type = PayloadType.jetton

class StonfiMessageSwapErrorReserveError(TlbScheme):
    """
    swap_error_reserve_error#38976e9b = JettonPayload;
    """
    def __init__(self):
        pass

    def serialize(self) -> Cell:
        builder = Builder()
        builder.store_uint(0x38976e9b, 32)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x38976e9b:
          raise ValueError(f"Not a StonSwapErrorReserveError, unknown operation: {op}")
        return cls()

    op = 0x38976e9b

    message_type = PayloadType.jetton

############################################################
# Ston.fi v2
class StonfiV2MessageSwap(TlbScheme):
    """
    swap#6664de2a token_wallet1:MsgAddress refund_address:MsgAddress excesses_address:MsgAddress tx_deadline:uint64 cross_swap_body:^[min_out:Coins receiver:MsgAddress fwd_gas:Coins custom_payload:(Maybe ^Cell) refund_fwd_gas:Coins refund_payload:(Maybe ^Cell) ref_fee:uint16 ref_address:MsgAddress] = JettonPayload;
    """
    def __init__(self,
                 token_wallet1: typing.Optional[Address] = None,
                 refund_address: typing.Optional[Address] = None,
                 excesses_address: typing.Optional[Address] = None,
                 tx_deadline: typing.Optional[int] = 0,
                 min_out: typing.Optional[int] = 0,
                 receiver: typing.Optional[Address] = None,
                 fwd_gas: typing.Optional[int] = 0,
                 custom_payload: typing.Optional[Cell] = None,
                 refund_fwd_gas: typing.Optional[int] = 0,
                 refund_payload: typing.Optional[Cell] = None,
                 ref_fee: typing.Optional[int] = 0,
                 ref_address: typing.Optional[Address] = None
                ):
        if isinstance(token_wallet1, str):
            token_wallet1 = Address(token_wallet1)
        if isinstance(refund_address, str):
            refund_address = Address(refund_address)
        if isinstance(excesses_address, str):
            excesses_address = Address(excesses_address)
        if isinstance(receiver, str):
            receiver = Address(receiver)
        if isinstance(ref_address, str):
            ref_address = Address(ref_address)
        self.token_wallet1 = token_wallet1
        self.refund_address = refund_address
        self.excesses_address = excesses_address
        self.tx_deadline = tx_deadline
        self.min_out = min_out
        self.receiver = receiver
        self.fwd_gas = fwd_gas
        self.custom_payload = custom_payload
        self.refund_fwd_gas = refund_fwd_gas
        self.refund_payload = refund_payload
        self.ref_fee = ref_fee
        self.ref_address = ref_address
    
    def serialize(self) -> Cell:
        cross_swap_body = Builder()
        cross_swap_body \
            .store_coins(self.min_out) \
            .store_address(self.receiver) \
            .store_coins(self.fwd_gas)
        cross_swap_body.store_bit(1).store_ref(self.custom_payload) if self.custom_payload is not None else cross_swap_body.store_bit(0)
        cross_swap_body.store_coins(self.refund_fwd_gas)
        cross_swap_body.store_bit(1).store_ref(self.refund_payload) if self.refund_payload is not None else cross_swap_body.store_bit(0)
        cross_swap_body.store_uint(self.ref_fee, 16).store_address(self.ref_address)
        cross_swap_body_cell = cross_swap_body.end_cell()
        
        builder = Builder()
        builder \
            .store_uint(0x6664de2a, 32) \
            .store_address(self.token_wallet1) \
            .store_address(self.refund_address) \
            .store_address(self.excesses_address) \
            .store_uint(self.tx_deadline, 64)
        builder.store_ref(cross_swap_body_cell)
        return builder.end_cell()
    
    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x6664de2a:
          raise ValueError(f"Not a StonSwap, unknown operation: {op}")
        token_wallet1=cell_slice.load_address()
        refund_address=cell_slice.load_address(),
        excesses_address=cell_slice.load_address()
        tx_deadline=cell_slice.load_uint(64)
        cross_swap_body = cell_slice.load_ref().begin_parse()
        min_out=cross_swap_body.load_coins()
        receiver=cross_swap_body.load_address()
        fwd_gas=cross_swap_body.load_coins()
        custom_payload=cross_swap_body.load_ref().begin_parse() if cross_swap_body.load_bit() else None
        refund_fwd_gas=cross_swap_body.load_coins()
        refund_payload=cross_swap_body.load_ref().begin_parse() if cross_swap_body.load_bit() else None
        ref_fee=cross_swap_body.load_uint(16)
        ref_address=cross_swap_body.load_address()
        return cls(token_wallet1=token_wallet1,
                   refund_address=refund_address,
                   excesses_address=excesses_address,
                   tx_deadline=tx_deadline,
                   min_out=min_out,
                   receiver=receiver,
                   fwd_gas=fwd_gas,
                   custom_payload=custom_payload,
                   refund_fwd_gas=refund_fwd_gas,
                   refund_payload=refund_payload,
                   ref_fee=ref_fee,
                   ref_address=ref_address)


class StonfiV2pTONTransfer(TlbScheme):
    """
    ton_transfer#01f3835d query_id:uint64 ton_amount:Coins refund_address:MsgAddress forward_payload:(Either Cell ^Cell) = InternalMsgBody;
    """

    def __init__(self,
                 query_id: typing.Optional[int] = 0,
                 ton_amount: typing.Optional[int] = 0,
                 refund_address: typing.Optional[Address] = None,
                 forward_payload: typing.Optional[Cell] = None
                 ):
        if isinstance(refund_address, str):
            refund_address = Address(refund_address)
        self.query_id = query_id
        self.ton_amount = ton_amount
        self.refund_address = refund_address
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        builder = Builder()
        builder \
            .store_uint(0x01f3835d, 32) \
            .store_uint(self.query_id, 64) \
            .store_coins(self.ton_amount) \
            .store_address(self.refund_address)
        builder.store_bit(1).store_cell(self.forward_payload) if self.forward_payload is not None else builder.store_bit(0)
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice):
        op = cell_slice.load_uint(32)
        if not op == 0x01f3835d:
          raise ValueError(f"Not a StonfiV2pTONTransfer, unknown operation: {op}")
        return cls(query_id=cell_slice.load_uint(64),
                   ton_amount=cell_slice.load_coins(),
                   refund_address=cell_slice.load_address(),
                   forward_payload=cell_slice.load_cell() if cell_slice.load_bit() else None)

    op = 0x01f3835d

    message_type = PayloadType.internal


############################################################
known_internal_opcodes = {}
known_jetton_opcodes = {}

import inspect, sys

for name, obj in inspect.getmembers(sys.modules[__name__]):
    # if opcode duplicates raise an error
    if inspect.isclass(obj) and hasattr(obj, 'op'):
        if obj.message_type == PayloadType.internal:
            if obj.op in known_internal_opcodes:
                raise ValueError(f"Duplicate opcode for internal {obj.op} found in {obj} and {known_internal_opcodes[obj.op]}")
            known_internal_opcodes[obj.op] = obj
        elif obj.message_type == PayloadType.jetton:
            if obj.op in known_jetton_opcodes:
                raise ValueError(f"Duplicate opcode for jetton payload {obj.op} found in {obj} and {known_jetton_opcodes[obj.op]}")
            known_jetton_opcodes[obj.op] = obj


############################################################
# Lets put all classes in separate namespaces for better readability (an use the same names)

Jetton = SimpleNamespace()
Jetton.Transfer = JettonTransfer
Jetton.TransferNotification = JettonTransferNotification
Jetton.Burn = JettonBurn
Jetton.Excesses = JettonExcesses
Jetton.BurnNotification = JettonBurnNotification
Jetton.InternalTransfer = JettonInternalTransfer

Dedust = SimpleNamespace()
Dedust.SwapParams = DedustSwapParams
Dedust.SwapStep = DedustSwapStep
Dedust.SwapKind = SwapKind
Dedust.SwapStepParams = DedustSwapStepParams
Dedust.Swap = DedustMessageSwap
Dedust.PoolType = DedustPoolType
Dedust.Asset = DedustAsset
Dedust.PoolParams = DedustPoolParams
Dedust.DepositLiquidity = DedustMessageDepositLiquidity
Dedust.PayoutFromPool = DedustMessagePayoutFromPool
Dedust.Payout = DedustMessagePayout
Dedust.JettonPayloadSwap = DedustJettonPayloadSwap
Dedust.JettonPayloadDepositLiquidity = DedustJettonPayloadDepositLiquidity
Dedust.CancelDeposit = DedustMessageCancelDeposit

Stonfi = SimpleNamespace()
Stonfi.Swap = StonfiMessageSwap
Stonfi.ProvideLiquidity = StonfiMessageProvideLiquidity
Stonfi.SwapSuccess = StonfiMessageSwapSuccess
Stonfi.SwapSuccessReferal = StonfiMessageSwapSuccessReferal
Stonfi.SwapErrorNoLiquidity = StonfiMessageSwapErrorNoLiquidity
Stonfi.SwapErrorReserveError = StonfiMessageSwapErrorReserveError

StonfiV2 = SimpleNamespace()
StonfiV2.Swap = StonfiV2MessageSwap
StonfiV2.pTON = SimpleNamespace()
StonfiV2.pTON.Transfer = StonfiV2pTONTransfer
