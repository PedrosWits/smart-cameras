from azure.storage.table import TableService, Entity

mykey = "umh7XfkHhN05Blx7+LltNoSZ8xr6qD7l5dJZ44LRJH6YoQ4sWvQ6D2lyl31h3RfOBS/YWdtUN5ZseAKTnSctpg=="
acc_name = "smartcamerasdiag952"

table_service = TableService(account_name=acc_name, account_key=mykey)
table_service.create_table('tasktable')

task = {'PartitionKey': 'helloworld', 'RowKey': '1', 'description' : 'Take out the trash', 'priority' : 200}
table_service.insert_entity('tasktable', task)

task2 = table_service.get_entity('tasktable', 'helloworld', '1')

print(task2.description)
