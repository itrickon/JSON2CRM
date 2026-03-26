import customtkinter as ctk
import requests
from datetime import datetime
from config import API_URL

# Неизменяемые поля
STATUS = "Перевели на оператора"
SOURCE = 394

# Настройки темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class PelotonApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JSON2CRM - PELETON")
        self.geometry("520x480")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        main_frame.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame,
            text="JSON2CRM",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Телефон
        self.phone_label = ctk.CTkLabel(
            main_frame,
            text="Телефон:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.phone_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        self.phone_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="79994440011",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.phone_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        self.phone_entry.insert(0, "79994440011")

        # Комментарий
        self.comment_label = ctk.CTkLabel(
            main_frame,
            text="Комментарий:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.comment_label.grid(row=3, column=0, sticky="w", pady=(0, 5))

        self.comment_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Имя Анатолий Lada largus new",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.comment_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 25))
        self.comment_entry.insert(0, "Имя Анатолий Lada largus new")

        # Статус (неизменяемое)
        status_container = ctk.CTkFrame(main_frame, fg_color="#2a2a3e", corner_radius=8)
        status_container.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        status_container.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            status_container,
            text="Статус:",
            font=ctk.CTkFont(size=12),
            fg_color="transparent"
        ).grid(row=0, column=0, padx=(12, 10), pady=10, sticky="w")

        ctk.CTkLabel(
            status_container,
            text=STATUS,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4ade80",
            fg_color="transparent",
            anchor="w"
        ).grid(row=0, column=1, pady=10, sticky="w")

        # Источник (неизменяемое)
        source_container = ctk.CTkFrame(main_frame, fg_color="#2a2a3e", corner_radius=8)
        source_container.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        source_container.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            source_container,
            text="Источник:",
            font=ctk.CTkFont(size=12),
            fg_color="transparent"
        ).grid(row=0, column=0, padx=(12, 10), pady=10, sticky="w")

        ctk.CTkLabel(
            source_container,
            text=str(SOURCE),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#fbbf24",
            fg_color="transparent",
            anchor="w"
        ).grid(row=0, column=1, pady=10, sticky="w")

        # Кнопка отправки
        self.send_btn = ctk.CTkButton(
            main_frame,
            text="Отправить в CRM 🚀",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.send_data,
            fg_color="#4a9eff",
            hover_color="#3a8eef"
        )
        self.send_btn.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Статус бар
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12),
            fg_color="transparent"
        )
        self.status_label.grid(row=8, column=0, columnspan=2)

        # Footer
        footer = ctk.CTkLabel(
            main_frame,
            text="API: dirty.crm-auto.ru/api/setRequestC",
            font=ctk.CTkFont(size=10),
            text_color="#606080",
            fg_color="transparent"
        )
        footer.grid(row=9, column=0, columnspan=2, sticky="s", pady=(0, 10))

    def send_data(self):
        phone = self.phone_entry.get().strip()
        comment = self.comment_entry.get().strip()

        if not phone or not comment:
            self.show_error("Заполните все поля!")
            return

        # createdAt - текущее время
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = {
            "phone": phone,
            "createdAt": created_at,
            "comment": comment,
            "status": STATUS,
            "source": SOURCE
        }

        # Блокируем кнопку на время отправки
        self.send_btn.configure(text="Отправка...", state="disabled")
        self.status_label.configure(text="")
        self.update()

        try:
            response = requests.post(API_URL, json=data, timeout=10)
            
            if response.status_code == 200:
                self.status_label.configure(
                    text="Успешно отправлено!",
                    text_color="#4ade80"
                )
                self.show_success("Данные отправлены в CRM!")
            else:
                self.status_label.configure(
                    text=f"Ошибка: {response.status_code}",
                    text_color="#f87171"
                )
                self.show_error(f"Код ответа: {response.status_code}\n{response.text}")
        except requests.exceptions.RequestException as e:
            self.status_label.configure(
                text="Ошибка соединения",
                text_color="#f87171"
            )
            self.show_error(f"Не удалось отправить данные:\n{str(e)}")
        finally:
            self.send_btn.configure(text="Отправить в CRM", state="normal")

    def show_success(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Успех")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)

        ctk.CTkLabel(
            dialog,
            text="✅" + message,
            font=ctk.CTkFont(size=14),
            text_color="#4ade80"
        ).pack(pady=20, padx=20)

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack(pady=10)

    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ошибка")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)

        ctk.CTkLabel(
            dialog,
            text="⚠️" + message,
            font=ctk.CTkFont(size=14),
            text_color="#f87171",
            wraplength=300,
            justify="center"
        ).pack(pady=20, padx=20)

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            fg_color="#f87171",
            hover_color="#dc2626",
            command=dialog.destroy
        ).pack(pady=10)


if __name__ == "__main__":
    app = PelotonApp()
    
    # Установка иконки
    try:
        app.iconbitmap("brand-json.ico")
    except:
        pass
    
    app.mainloop()
