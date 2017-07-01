import boto3
from datetime import datetime


class EC2Manager(object):

    def __init__(self):
        self.ec2_handler = boto3.client('ec2')
        self.reservations = self.get_reservations()

    def get_reservations(self):
        print self.ec2_handler.describe_instances().get('Reservations', [])
        return self.ec2_handler.describe_instances().get('Reservations', [])

    def get_active_instance_count(self):
        active_counter = 0
        print self.reservations
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                if instance.get('State', {}).get('Name') == 'running':
                    active_counter += 1
        return active_counter

    def get_active_instance_names(self):
        active_instance_list = list()
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                if instance.get('State', {}).get('Name') == 'running':
                    active_instance_list.append(instance.get('Tags', [{}])[0].get('Value', ''))
        return active_instance_list

    def get_instance_id(self, server_name):
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                if instance.get('Tags', [{}])[0].get('Value') == server_name:
                    return instance.get('InstanceId')

    def start_server(self, server_name):
        instance_id = self.get_instance_id(server_name)
        self.ec2_handler.start_instances(InstanceIds=[instance_id])

    def stop_server(self, server_name):
        instance_id = self.get_instance_id(server_name)
        self.ec2_handler.stop_instances(InstanceIds=[instance_id])

    def get_all_server_names(self):
        instance_names = list()
        for reservation in self.reservations:
            instance_list = reservation.get('Instances', [])
            for instance in instance_list:
                instance_names.append(instance.get('Tags', [{}])[0].get('Value', ''))
        return instance_names


class RDSManager(object):

    def __init__(self):
        self.rds_handler = boto3.client('rds')
        self.rds_info = self.get_rds_info()

    def get_rds_info(self):
        return self.rds_handler.describe_db_instances()

    def get_rds_names(self):
        db_instances = self.rds_info.get('DBInstances')
        return map(lambda instance: instance.get('DBInstanceIdentifier'), db_instances)

    def create_rds_snapshot(self, instance_identifier):
        snapshot_identifier = instance_identifier + '-' + datetime.now().strftime('%Y-%m-%d-%H-%M')
        self.rds_handler.create_db_snapshot(DBInstanceIdentifier=instance_identifier,
                                            DBSnapshotIdentifier=snapshot_identifier)


class SNSManager(object):

    def __init__(self):
        self.sns_handler = boto3.client('sns')

    def send_sms(self):
        response = self.sns_handler.publish(
                        PhoneNumber='+919819476633',
                        Message='This is a test SMS message')
        print response

# #     def main(self):
# #         print self.get_rds_names()
# # #         self.reservations = self.get_reservations()
# # #         print self.reservations
# # #         server_names = self.get_all_server_names()
# # #         print server_names
# # #         # self.reservations = self.get_reservations()
# # #         # print 'Active instance count : %s' % self.get_active_instance_count()
# # #         # print 'Active instance names : %s' % '\n'.join(self.get_active_instance_names())
# # #         # self.start_server('jenkins')
# # #         # print 'Active instance names : %s' % '\n'.join(self.get_active_instance_names())
# # #
# # class_obj = EC2Manager()
# # class_obj.main()
# class_obj = SNSManager()
# class_obj.send_sms()