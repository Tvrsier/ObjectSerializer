import requests

def fetch_data_from_api(api_url):
    try:
        # Effettua la richiesta GET all'API
        response = requests.get(api_url)

        # Verifica se la richiesta ha avuto successo
        if response.status_code == 200:
            # Parsing del contenuto della risposta come JSON
            json_data = response.json()

            return json_data
        else:
            print(f"Errore {response.status_code}: impossibile ottenere i dati dall'API.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta HTTP: {e}")
        return None
