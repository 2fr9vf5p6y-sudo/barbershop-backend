from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Master:
    master_id: int
    name: str


@dataclass(frozen=True)
class Service:
    service_id: int
    name: str
    price: int


class Appoinment:
    def __init__(self, appointment_id: int, client_name: str, master_id: int,
                 service_id: int, time: str):
        self.id = appointment_id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time

    def __repr__(self):
        return (
            f"Appoinment(id={self.id}, client_name={self.client_name!r}, "
            f"master_id={self.master_id}, service_id={self.service_id}, "
            f"time={self.time!r})"
        )


masters = [
    Master(1, "Алексей Морозов"),
    Master(2, "Дмитрий Иванов"),
]

services = [
    Service(1, "Мужская стрижка", 2200),
    Service(2, "Оформление бороды", 1000),
]

appointments: list[Appoinment] = []


def get_master(master_id: int) -> Master | None:
    return next((master for master in masters if master.master_id == master_id), None)


def get_service(service_id: int) -> Service | None:
    return next((service for service in services if service.service_id == service_id), None)


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str,
) -> Appoinment | None:
    if not isinstance(client_name, str) or not client_name.strip():
        return None
    if type(master_id) is not int or type(service_id) is not int:
        return None
    if not isinstance(time, str):
        return None

    master = get_master(master_id)
    service = get_service(service_id)
    if master is None or service is None:
        return None

    try:
        if len(time) != 5 or time[2] != ":":
            return None
        parsed_time = datetime.strptime(time, "%H:%M").time()
        if parsed_time.strftime("%H:%M") != time:
            return None
    except ValueError:
        return None

    if not ("08:00" <= time <= "20:00"):
        return None

    for item in appointments:
        if item.master_id == master.master_id and item.time == time:
            return None

    appointment = Appoinment(
        len(appointments) + 1,
        client_name.strip(),
        master.master_id,
        service.service_id,
        time,
    )
    appointments.append(appointment)
    return appointment


def main() -> None:
    first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

    print("Список записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)

    assert isinstance(first_appointment, Appoinment)
    assert isinstance(second_appointment, Appoinment)

    invalid_name = create_appointment("", 1, 1, "12:00")
    invalid_time = create_appointment("Сидорова А.А.", 1, 1, "00:00")
    assert invalid_name is None and invalid_time is None
    print("Количество записей:", len(appointments))


if __name__ == "__main__":
    main()
