class DataPublisher:
    def __init__(self, powerbi_client):
        self.powerbi_client = powerbi_client

    def publish_data(self, dataset_id, data):
        """
        Publishes the processed data to Power BI.

        :param dataset_id: The ID of the dataset in Power BI.
        :param data: The data to be published.
        """
        try:
            response = self.powerbi_client.push_data(dataset_id, data)
            if response.status_code == 200:
                print("Data published successfully to Power BI.")
            else:
                print(f"Failed to publish data: {response.content}")
        except Exception as e:
            print(f"An error occurred while publishing data: {str(e)}")