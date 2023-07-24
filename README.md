# Clone o projeto
git clone https://github.com/danbsilva/CodeGoup.git

# Path: CodeGoup
cd CodeGoup 

# Crie um ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Preencha o arquivo .env com as necessidades do seu projeto
LINKEDIN_USER=linkedin_user

LINKEDIN_PWD=linkedin_pwd

API_KEY_OPENWEATHERMAP=api_key_openweathermap

SMTP_SERVER=smtp.gmail.com

SMTP_PORT=587

SMTP_USERNAME=smtp_username

SMTP_PASSWORD=smtp_password

FROM_ADDR=from_addr

# Execute o comando abaixo para rodar o projeto
python3 main.py