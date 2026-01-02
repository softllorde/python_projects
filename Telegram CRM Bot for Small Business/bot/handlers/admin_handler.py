from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states.client import ClientStates
from bot.services.user_service import UserService
from bot.services.client_service import ClientService
from bot.keyboards.admin_keyboard import admin_keyboard
from bot.keyboards.confirm_keyboard import confirm_delete_keyboard
from bot.keyboards.status_keyboard import status_keyboard
from bot.constants.statuses import ClientStatus

client_service = ClientService()
user_service = UserService()

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_panel(message: types.Message):
	if not await user_service.is_admin(message.from_user.id):
		await message.answer("Доступ запрещен!")
		return
	await message.answer("Админ панель: \n/add_client имя номер_телефона - добавить клиента\n/set_status номер_телефона статус - установить статус клиента\n/delete_client номер_телефона - удалить клиента", reply_markup=admin_keyboard)

@admin_router.message(Command("add_client"))
async def add_client(message: types.Message):
    if not await user_service.is_admin(message.from_user.id):
        await message.answer("Доступ запрещён")
        return

    try:
        _, name, phone = message.text.split(maxsplit=2)
        await client_service.create_client(name, phone)
        await message.answer("Клиент добавлен")
    except ValueError as e:
        await message.answer(str(e))
    except Exception:
        await message.answer("Неверный формат команды")

@admin_router.message(Command("clients"))
async def list_clients(message: types.Message):
    if not await user_service.is_admin(message.from_user.id):
        await message.answer("Доступ запрещён")
        return

    clients = await client_service.get_all_clients()

    if not clients:
        await message.answer("Список пуст")
        return

    text = "\n".join(
        f"{c.name} | {c.phone} | {c.status}"
        for c in clients
    )

    await message.answer(text)

@admin_router.message(Command("set_status"))
async def set_status(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Введите номер клиента:")
    await state.set_state(ClientStates.waiting_for_status_phone)
    await cb.answer()

@admin_router.message(Command("delete_client"))
async def delete_client(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Введите номер клиента для удаления:")
    await state.set_state(ClientStates.waiting_for_delete_phone)
    await cb.answer()

@admin_router.callback_query(F.data == "add_client")
async def add_client(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Введите имя клиента:")
    await state.set_state(ClientStates.waiting_for_name)
    await cb.answer()

@admin_router.message(ClientStates.waiting_for_name)
async def client_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(ClientStates.waiting_for_phone)

@admin_router.message(ClientStates.waiting_for_phone)
async def client_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await client_service.create_client(
            name=data["name"],
            phone=message.text
        )
        await message.answer("Клиент добавлен", reply_markup=admin_keyboard)
    except ValueError as e:
        await message.answer(str(e), reply_markup=admin_keyboard)

    await state.clear()

@admin_router.callback_query(F.data == "list_clients")
async def list_clients(cb: CallbackQuery):
    clients = await client_service.get_all_clients()

    if not clients:
        await cb.message.answer("Клиентов нет")
    else:
        text = "\n".join(
            f"{c.name} | {c.phone} | {c.status or '—'}"
            for c in clients
        )
        await cb.message.answer(text)

    await cb.answer()

@admin_router.callback_query(F.data == "set_status")
async def set_status(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Введите номер клиента:")
    await state.set_state(ClientStates.waiting_for_status_phone)
    await cb.answer()

@admin_router.message(ClientStates.waiting_for_status_phone)
async def status_phone(message: Message, state: FSMContext):
    phone = message.text

    client = await client_service.get_client_by_phone(phone)
    if not client:
        await message.answer("Клиент не найден", reply_markup=admin_menu())
        await state.clear()
        return

    await state.update_data(phone=phone)

    text = (
        "Выберите новый статус клиента:\n\n"
        f"Имя: {client.name}\n"
        f"Телефон: {client.phone}\n"
        f"Текущий статус: {client.status or '—'}"
    )

    await message.answer(
        text,
        reply_markup=status_keyboard()
    )
    await state.set_state(ClientStates.waiting_for_status_choice)

@admin_router.message(ClientStates.waiting_for_status_value)
async def status_value(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await client_service.update_status(
            phone=data["phone"],
            status=message.text
        )
        await message.answer("Статус обновлён", reply_markup=admin_keyboard)
    except ValueError as e:
        await message.answer(str(e), reply_markup=admin_keyboard)

    await state.clear()

@admin_router.callback_query(F.data == "delete_client")
async def delete_client(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Введите номер клиента для удаления:")
    await state.set_state(ClientStates.waiting_for_delete_phone)
    await cb.answer()

@admin_router.message(ClientStates.waiting_for_delete_phone)
async def delete_phone(message: Message, state: FSMContext):
    phone = message.text

    client = await client_service.get_client_by_phone(phone)
    if not client:
        await message.answer("Клиент не найден", reply_markup=admin_menu())
        await state.clear()
        return

    await state.update_data(phone=phone)

    text = (
        "Вы уверены, что хотите удалить клиента?\n\n"
        f"Имя: {client.name}\n"
        f"Телефон: {client.phone}\n"
        f"Статус: {client.status or '—'}"
    )

    await message.answer(
        text,
        reply_markup=confirm_delete_keyboard()
    )
    await state.set_state(ClientStates.confirm_delete)

@admin_router.message(ClientStates.waiting_for_delete_phone)
async def delete_phone(message: Message, state: FSMContext):
    phone = message.text

    client = await client_service.get_client_by_phone(phone)
    if not client:
        await message.answer("Клиент не найден", reply_markup=admin_keyboard)
        await state.clear()
        return

    await state.update_data(phone=phone)

    text = (
        "Вы уверены, что хотите удалить клиента?\n\n"
        f"Имя: {client.name}\n"
        f"Телефон: {client.phone}\n"
        f"Статус: {client.status or '—'}"
    )

    await message.answer(
        text,
        reply_markup=confirm_delete_keyboard()
    )
    await state.set_state(ClientStates.confirm_delete)

@admin_router.callback_query(F.data == "confirm_delete_yes", ClientStates.confirm_delete)
async def confirm_delete_yes(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phone = data["phone"]

    try:
        await client_service.delete_client(phone)
        await cb.message.answer("Клиент успешно удалён", reply_markup=admin_keyboard)
    except ValueError as e:
        await cb.message.answer(str(e), reply_markup=admin_keyboard)

    await state.clear()
    await cb.answer()

@admin_router.callback_query(F.data == "confirm_delete_no", ClientStates.confirm_delete)
async def confirm_delete_no(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Удаление отменено", reply_markup=admin_keyboard)
    await state.clear()
    await cb.answer()

@admin_router.callback_query(F.data.startswith("status:"),ClientStates.waiting_for_status_choice)
async def status_chosen(cb: CallbackQuery, state: FSMContext):
    status_key = cb.data.split(":")[1]

    status = ClientStatus[status_key].value

    data = await state.get_data()
    phone = data["phone"]

    try:
        await client_service.update_status(phone, status)
        await cb.message.answer(
            f"Статус обновлён: {status}",
            reply_markup=admin_keyboard
        )
    except ValueError as e:
        await cb.message.answer(str(e), reply_markup=admin_keyboard)

    await state.clear()
    await cb.answer()
