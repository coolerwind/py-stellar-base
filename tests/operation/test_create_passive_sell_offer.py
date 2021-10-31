from decimal import Decimal

import pytest

from stellar_sdk import CreatePassiveSellOffer, Operation, Price

from . import *


class TestCreatePassiveSellOffer:
    @pytest.mark.parametrize(
        "amount, price, source, xdr",
        [
            pytest.param(
                "100",
                "1",
                None,
                "AAAAAAAAAAQAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAAB",
                id="without_source",
            ),
            pytest.param(
                "100",
                "1",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAQAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAAB",
                id="with_source_public_key",
            ),
            pytest.param(
                "100",
                "1",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABAAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAQAAAAE=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "100",
                "1",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABAAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAQAAAAE=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                Decimal("100"),
                "1",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAQAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAAB",
                id="amount_decimal",
            ),
            pytest.param(
                "100",
                Decimal("1"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAQAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAAB",
                id="price_decimal",
            ),
            pytest.param(
                "100",
                Price(1, 1),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAQAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAAB",
                id="price_object",
            ),
        ],
    )
    def test_xdr(self, amount, price, source, xdr):
        selling = native_asset
        buying = asset1
        op = CreatePassiveSellOffer(selling, buying, amount, price, source)
        assert op.buying == buying
        assert op.selling == selling
        assert op.amount == str(amount)
        assert (
            op.price == price
            if isinstance(price, Price)
            else Price.from_raw_price(str(price))
        )
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
