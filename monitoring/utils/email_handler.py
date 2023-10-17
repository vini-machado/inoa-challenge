from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
class Email:
    def __init__(self, tunnel_actions: pd.DataFrame) -> None:
        self.tunnel_actions = tunnel_actions

    @property
    def to_send(self):
        emails_data = self.tunnel_actions.groupby(['email', 'action'])['Ticker'].apply(list).reset_index()
        return emails_data.to_dict('records')
    
    def __message(self, action: str, tickers: list[str]) -> str:
        BASE_BUY_MESSAGE  = "These stocks reached buy price: "
        BASE_SELL_MESSAGE = "These stocks reached sell price: "

        tickers_str = ", ".join(tickers)
        
        if action == 'Sell':
            return BASE_SELL_MESSAGE + tickers_str
        if action == 'Buy':
            return BASE_BUY_MESSAGE + tickers_str
        
        return "Contact Administration"
    
    def __subject(self, action: str) -> str:
        BASE_SUBJECT = "Tickers to "

        return BASE_SUBJECT + action


    def send(self) -> None:

        for email_msg in self.to_send:
            email = []
            email.append(email_msg['email'])

            subject = self.__subject(email_msg['action'])
            message = self.__message(email_msg['action'], email_msg['Ticker'])


            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                email,
                fail_silently=False,
            )

            
