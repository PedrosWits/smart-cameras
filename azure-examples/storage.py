from azure.storage.table import TableService, Entity

mykey = "uk/kCVQbU+52lixEtQFw0Xjk5XkC2RYzJ8BzBG22i2x3XfrIVBs1HgyBOO1csaf3ozG34Arj6Z+0kZcN0nEMiw=="
acc_name = "smartcamerasdisks221"

table_service = TableService(account_name=acc_name, account_key=mykey)
table_service.create_table('tasktable')

task = {'PartitionKey': 'helloworld', 'RowKey': '1', 'description' : 'Take out the trash', 'priority' : 200}
table_service.insert_entity('tasktable', task)

task2 = table_service.get_entity('tasktable', 'helloworld', '1')

print(task2.description)
