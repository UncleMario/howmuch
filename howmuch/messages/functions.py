from django.contrib.auth.models import User
from django.core.mail import send_mail
from howmuch.core.models import Assignment, RequestItem
from howmuch.messages.models import Conversation, Message

class InitialConversationContext:
	def __init__(self,buyer,saller, conversation):
		self.buyer = buyer
		self.saller = saller
		self.conversation = conversation

	def createMessageByBuyer(self):
		"""
		Se crea el mensaje de inicio del comprador
		"""
		theMessage = "Hola " + str(self.saller.first_name) + ", la Direccion a la que quiero que envies el producto es: " + str(self.buyer.get_profile().getAddressDelivery()) 
		newMessage = Message.objects.create(owner = self.buyer, message = theMessage ,conversation = self.conversation )
		newMessage.save()

		"""
		se envia un mail con el mensaje de inicio del comprador para el vendedor
		"""

		subject = 'Direccion de envio del articulo %s' % (self.conversation.assignment.requestItem.title)
		message = theMessage
		de = ''
		to = [str(self.saller.email)] 

		send_mail(subject,message,de,to)


	def createMessageBySaller(self):
		theMessage = "Gracias, mi Banco es: " + str(self.saller.get_profile().bank) + " y mi CTA es: " + str(self.saller.get_profile().account_bank) + " , En cuanto este confirmado el Deposito, yo te enviare el Producto"
		newMessage = Message.objects.create(owner = self.saller, message = theMessage, conversation = self.conversation)
		newMessage.save()

		"""
		se envia un mail con el mensaje de inicio del vendedor para el comprador
		"""
		
		subject = 'Informacion de pago para el articulo %s' % (self.conversation.assignment.requestItem.title)
		message = theMessage
		de = ''
		to = [str(self.buyer.email)] 

		send_mail(subject,message,de,to)


class ConversationFeatures:
	def __init__(self, conversation, user):
		self.conversation = conversation
		self.user = user

	def is_inside(self):
		if self.conversation.assignment.owner == self.user or self.conversation.assignment.requestItem.owner == self.user:
			return True
		else:
			return False




