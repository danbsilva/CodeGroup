from src.linkedin import Linkedin
from decouple import config
import pandas as pd
from src import schemas
from src import apis
from src import mail
from src.logging import Logging

path_collaborators = 'Colaboradores.xlsx'


def main():

    # Create instance of LinkedIn class
    linkedin = Linkedin()
    api = apis.API()
    logging = Logging()  # Create instance of Logging class

    logging.info('Starting the automation')  # Logging the start of automation

    # Login in Linkedin
    login = linkedin.login(config('LINKEDIN_USER'), config('LINKEDIN_PWD'))
    if True in login:  # If login is successfully
        # Read the file with the collaborators
        collaborators = pd.read_excel(path_collaborators)

        # Fill the NaN values with empty string
        collaborators.fillna('', inplace=True)
        email_collaborators = []  # List of collaborators to send e-mail

        # Iterate over the rows of collaborators
        for index, row in collaborators.iterrows():

            # Create instance of Collaborator class
            collaborator = schemas.Collaborator(
                name=row['Colaborador'],
                city=row['Cidade'],
                state=row['Estado'],
                description=row['Descrição'],
                office=row['Cargo'],
                company=row['Empresa'],
                climate=row['Clima']
            )

            # Search the collaborator in LinkedIn
            search_collaborator = linkedin.search_collaborator(collaborator)

            if True in search_collaborator:  # If collaborator is found

                # Search the description of collaborator in LinkedIn
                search_description = linkedin.search_description(collaborator)

                if True in search_description:  # If description is found

                    # Search the office and company of collaborator in LinkedIn
                    search_office_and_company = linkedin.search_office_and_company(collaborator)

                    if True in search_office_and_company:  # If office and company is found

                        # Search the climate of collaborator in API
                        climate = api.climate(collaborator.city)
                        try:
                            description_climate = climate['weather'][0]['description']
                            temperature_climate = climate['main']['temp'] - 273.15
                            collaborator.climate = f"{description_climate} - {temperature_climate:.2f}°C"
                            logging.info(
                                f'Climate of {collaborator.name} found!')  # Logging the climate found
                        except Exception:
                            collaborator.climate = 'Não encontrado'
                            logging.warning(
                                f'Climate of {collaborator.name} not found!')  # Logging the climate not found

                        # Update the collaborator in the file
                        collaborators.loc[index, 'Descrição'] = collaborator.description
                        collaborators.loc[index, 'Cargo'] = collaborator.office
                        collaborators.loc[index, 'Empresa'] = collaborator.company
                        collaborators.loc[index, 'Clima'] = collaborator.climate

                        # Save the file
                        collaborators.to_excel('src/Colaboradores.xlsx', index=False)

                        email_collaborators.append(collaborator)  # Add the collaborator in the list of collaborators to send e-mail

        # Send the e-mail with the file
        mail.sendmail('danilloaugustobsilva@hotmail.com','Resultado', email_collaborators, path_collaborators)

        logging.info('Automation finished successfully')  # Logging the end of automation


if __name__ == '__main__':
    main()
