from datetime import datetime
import pandas as pd

class CustomModel:
    def __init__(self, model, dataset, numeric_attributes, one_hot_attributes, colunas_finais):
        self.model = model

        # Processar os atributos para incluir as datas ao invés da idade
        self.attributes_info = {}
        self.valid_options = {}  # Dicionário para armazenar opções válidas
        self.numeric_attributes = numeric_attributes  # Lista de atributos que precisam ser validados como numéricos
        self.one_hot_attributes = one_hot_attributes
        self.colunas_finais = colunas_finais

        for column in dataset.columns:
            if column == "age":
                self.attributes_info["mothers_birth_date"] = "Data"
                self.attributes_info["date_start_pregnancy"] = "Data"
                self.valid_options["mothers_birth_date"] = ["YYYY-MM-DD"]
                self.valid_options["date_start_pregnancy"] = ["YYYY-MM-DD"]
            elif column == "target":
                continue
            else:
                if '.' in column:
                  base_column = column.rsplit('_', 1)[0]  # Pegar o início da coluna até o último '_'
                else:
                    base_column = column

                self.attributes_info[base_column] = dataset[column].dtype
                self.valid_options[base_column] = dataset[column].unique().tolist()

        self.pre_processing_steps = [
            self.calculate_age,
            self.one_hot_enconding
        ]

    def calculate_age(self, birth_date, notification_date):
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        notification_date = datetime.strptime(notification_date, "%Y-%m-%d")
        age = notification_date.year - birth_date.year - ((notification_date.month, notification_date.day) < (birth_date.month, birth_date.day))
        return age

    def one_hot_enconding(self, data):
        df = pd.DataFrame(data, index=[0])
        df = pd.get_dummies(df, columns=self.one_hot_attributes)
        df_entrada_encoded = df.reindex(columns=self.colunas_finais, fill_value=0)
        dict_from_df = df_entrada_encoded.to_dict(orient='records')[0]
        return dict_from_df

    def preprocess(self, data):
        processed_data = {}
        for attribute in self.attributes_info.keys():
            if attribute == "date_start_pregnancy":
                continue
            if attribute == "mothers_birth_date":
                processed_data["idade"] = self.calculate_age(data["mothers_birth_date"], data["date_start_pregnancy"])
            else:
                value = data.get(attribute)
                if attribute in self.numeric_attributes:
                    if not isinstance(value, (int, float)):
                        raise ValueError(f"Invalid numeric value for {attribute}: {value}")
                else:
                    if value not in self.valid_options.get(attribute, [value]):
                        raise ValueError(f"Invalid value for {attribute}: {value}")
                processed_data[attribute] = value

        processed_data = self.one_hot_enconding(processed_data)

        return processed_data