# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .envelope_type import EnvelopeType
from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .transaction_v0_envelope import TransactionV0Envelope
from .transaction_v1_envelope import TransactionV1Envelope

__all__ = ["TransactionEnvelope"]


class TransactionEnvelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union TransactionEnvelope switch (EnvelopeType type)
    {
    case ENVELOPE_TYPE_TX_V0:
        TransactionV0Envelope v0;
    case ENVELOPE_TYPE_TX:
        TransactionV1Envelope v1;
    case ENVELOPE_TYPE_TX_FEE_BUMP:
        FeeBumpTransactionEnvelope feeBump;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: EnvelopeType,
        v0: TransactionV0Envelope = None,
        v1: TransactionV1Envelope = None,
        fee_bump: FeeBumpTransactionEnvelope = None,
    ) -> None:
        self.type = type
        self.v0 = v0
        self.v1 = v1
        self.fee_bump = fee_bump

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX_V0:
            self.v0.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            self.v1.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            self.fee_bump.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionEnvelope":
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX_V0:
            v0 = TransactionV0Envelope.unpack(unpacker)
            return cls(type, v0=v0)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            v1 = TransactionV1Envelope.unpack(unpacker)
            return cls(type, v1=v1)
        if type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            fee_bump = FeeBumpTransactionEnvelope.unpack(unpacker)
            return cls(type, fee_bump=fee_bump)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionEnvelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionEnvelope":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.v0 == other.v0
            and self.v1 == other.v1
            and self.fee_bump == other.fee_bump
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        out.append(f"fee_bump={self.fee_bump}") if self.fee_bump is not None else None
        return f"<TransactionEnvelope {[', '.join(out)]}>"