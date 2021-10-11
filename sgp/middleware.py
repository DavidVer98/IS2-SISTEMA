from django.shortcuts import redirect
from django.urls import reverse


class VerificarUsuario:

    def __init__(self,get_response):
        """Middleware initialization """
        self.get_response = get_response

    def __call__(self, request):
        """ Code to be executed for each request before the view is called """
        if not request.user.is_anonymous:
            #print("no es anonimo")
            if not request.user.is_staff:
                    # user = request.user.profile
                   # print("no es parte del staff ", profile.esta_activo)
                    if  request.user.estaActivado == False:
                        #print("hola??")
                        if request.path not in [reverse('login'), reverse('logout'), reverse('activar')]:
                            #print("entro?")

                            return redirect('activar')

        response = self.get_response(request)
        return response