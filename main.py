from api import app
from py_eureka_client import eureka_client

# Parametros para o eureka
eureka_server = 'http://54.91.53.248:8761/eureka'
app_name = 'modelo-morte-fetal'
instance_host = '54.91.53.248'
instance_port = 5001

# Inicializando o Eureka
eureka_client.init(eureka_server=eureka_server, app_name=app_name,
                  instance_host=instance_host, instance_port=instance_port,
                  status_page_url="/api/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=instance_port, debug=True)
    
