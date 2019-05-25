import injector
from sqlalchemy.engine import Connection

from foundation.events import AsyncEventHandlerProvider, AsyncHandler, EventBus

from payments.config import PaymentsConfig
from payments.events import PaymentCaptured, PaymentCharged, PaymentFailed, PaymentStarted
from payments.facade import PaymentsFacade

__all__ = [
    "Payments",
    "PaymentsConfig",
    "PaymentsFacade",
    "PaymentStarted",
    "PaymentCharged",
    "PaymentCaptured",
    "PaymentFailed",
]


class Payments(injector.Module):
    @injector.provider
    def facade(self, config: PaymentsConfig, connection: Connection, event_bus: EventBus) -> PaymentsFacade:
        return PaymentsFacade(config, connection, event_bus)

    def configure(self, binder: injector.Binder) -> None:
        binder.multibind(AsyncHandler[PaymentCharged], to=AsyncEventHandlerProvider(PaymentChargedHandler))


class PaymentChargedHandler:
    @injector.inject
    def __init__(self, facade: PaymentsFacade) -> None:
        self._facade = facade

    def __call__(self, event: PaymentCharged) -> None:
        print("TODO")
        self._facade.capture_payment(event.payment_uuid, event.customer_id)
