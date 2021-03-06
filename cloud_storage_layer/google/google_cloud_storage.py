"""
AWS SDK for Python (Boto3) to create, configure, and manage AWS services,
such as Amazon Elastic Compute Cloud (Amazon EC2) and Amazon Simple Storage Service (Amazon S3)
"""
import json

from project_library_layer.credentials.credential_data import get_google_cloud_storage_credentials
from project_library_layer.initializer.initializer import Initializer
from exception_layer.generic_exception.generic_exception import GenericException as GoogleCloudException
import sys, os
import dill
import io
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account


class GoogleCloudStorage:

    def __init__(self, bucket_name=None, region_name=None):
        """

        :param bucket_name:specify bucket name
        :param region_name: specify region name
        """
        try:
            initial = Initializer()
            if bucket_name is None:
                self.bucket_name = initial.get_google_bucket_name()
            else:
                self.bucket_name = bucket_name
            credentials = service_account.Credentials.from_service_account_info(
                get_google_cloud_storage_credentials()
            )
            self.client = storage.Client(credentials=credentials)
            existing_bucket_name = [bucket.name for bucket in self.client.list_buckets()]
            if self.bucket_name not in existing_bucket_name:
                self.bucket = self.client.create_bucket(self.bucket_name)
            else:
                self.bucket = self.client.get_bucket(self.bucket_name)

        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create object of GoogleCloudStorage in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            "__init__"))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def add_param(self, acceptable_param, additional_param):
        """

        :param acceptable_param: specify param list can be added
        :param additional_param: accepts a dictionary object
        :return: list of param added to current instance of class
        """
        try:
            self.__dict__.update((k, v) for k, v in additional_param.items() if k in acceptable_param)
            return [k for k in additional_param.keys() if k in acceptable_param]
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to add parameter in object in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.add_param.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def filter_param(self, acceptable_param, additional_param):
        """

        :param acceptable_param: specify param list can be added
        :param additional_param: accepts a dictionary object
        :return: dict of param after filter
        """
        try:
            accepted_param = {}
            accepted_param.update((k, v) for k, v in additional_param.items() if k in acceptable_param)
            return accepted_param
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to filter parameter in object in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.filter_param.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def remove_param(self, param):
        """

        :param param: list of param argument need to deleted from instance object
        :return True if deleted successfully else false:
        """
        try:
            for key in param:
                self.__dict__.pop(key)
            return True

        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to remove parameter in object in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.remove_param.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def list_directory(self, directory_full_path=None):
        """
        :param directory_full_path:directory path
        :return:
        {'status': True/False, 'message': 'message detail'
                    , 'directory_list': directory_list will be added if status is True}
        """
        try:
            if directory_full_path == "" or directory_full_path == "/" or directory_full_path is None:
                directory_full_path = ""
            else:
                if directory_full_path[-1] != "/":
                    directory_full_path += "/"

            is_directory_exist = False
            directory_list = []
            for key in self.client.list_blobs(self.bucket_name, prefix=directory_full_path):
                is_directory_exist = True
                dir_name = str(key.name).replace(directory_full_path, "")
                slash_index = dir_name.find("/")
                if slash_index >= 0:
                    name_after_slash = dir_name[slash_index + 1:]
                    if len(name_after_slash) <= 0:
                        directory_list.append(dir_name)
                else:
                    if dir_name != "":
                        directory_list.append(dir_name)
            if is_directory_exist:
                return {'status': True, 'message': 'Directory [{0}]  exist'.format(directory_full_path)
                    , 'directory_list': directory_list}
            else:
                return {'status': False, 'message': 'Directory [{0}] does not exist'.format(directory_full_path)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to list directory in object in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.list_directory.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def list_files(self, directory_full_path):
        """

        :param directory_full_path: directory
        :return:
        {'status': True/False, 'message': 'message detail'
                    , 'files_list': files_list will be added if status is True}
        """
        try:
            if directory_full_path == "" or directory_full_path == "/" or directory_full_path is None:
                directory_full_path = ""
            else:
                if directory_full_path[-1] != "/":
                    directory_full_path += "/"

            is_directory_exist = False
            list_files = []
            for key in self.client.list_blobs(self.bucket_name, prefix=directory_full_path):
                is_directory_exist = True
                file_name = str(key.name).replace(directory_full_path, "")
                if "/" not in file_name and file_name != "":
                    list_files.append(file_name)
            if is_directory_exist:
                return {'status': True, 'message': 'Directory [{0}]  present'.format(directory_full_path)
                    , 'files_list': list_files}
            else:
                return {'status': False, 'message': 'Directory [{0}] is not present'.format(directory_full_path)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to list files in object in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.list_files.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def list_buckets(self):
        """

        :return: All bucket names available in your gcp cloud storage
        {'status':True,'message':'message','bucket_list':'bucket_list}
        """
        try:
            existing_bucket = [bucket.name for bucket in self.client.list_buckets()]
            return {'status': True, 'message': 'Bucket retrived', 'bucket_list': existing_bucket}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to list bucket in object in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.list_buckets.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def create_bucket(self, bucket_name, over_write=False):
        """

        :param bucket_name: Name of bucket
        :param over_write: If true then existing bucket content will be removed
        :return: True if created else False
        """
        try:
            bucket_list = [bucket.name for bucket in self.client.list_buckets()]
            if bucket_name not in bucket_list:
                self.client.create_bucket(bucket_name)
                return {'status': True, 'message': "Bucket {0} created successfully".format(bucket_name)
                        }
            else:
                return {'status': False, 'message': "Bukcet {0} alredy exists".format(bucket_name)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create bucket in object in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.create_bucket.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def create_directory(self, directory_full_path, over_write=False, **kwargs):
        """

        :param directory_full_path: provide full directory path along with name
        :param over_write: default False if accept True then overwrite existing directory if exist
        :return {'status': True/False, 'message': 'message detail'}
        """
        try:
            if directory_full_path == "" or directory_full_path == "/" or directory_full_path is None:
                return {'status': False, 'message': 'Provide directory name'}
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.list_directory(directory_full_path)

            if over_write and response['status']:
                self.remove_directory(directory_full_path)
            if not over_write:
                if response['status']:
                    return {'status': False, 'message': 'Directory is already present. try with overwrite option.'}

            possible_directory = directory_full_path[:-1].split("/")

            directory_name = ""
            for dir_name in possible_directory:
                directory_name += dir_name + "/"
                response = self.list_directory(directory_name)
                if not response['status']:
                    self.bucket.blob(directory_name).upload_from_string("")
            return {'status': True, 'message': 'Directory [{0}] created successfully '.format(directory_full_path)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create directory in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.create_directory.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def remove_directory(self, directory_full_path):
        """

        :param directory_full_path:provide full directory path along with name
        kindly provide "" or "/" to remove all directory and file from bucket.
        :return:  {'status': True/False, 'message': 'message detail'}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            is_directory_found = False
            prefix_file_name = directory_full_path
            for blob in self.client.list_blobs(self.bucket_name, prefix=directory_full_path):
                is_directory_found = True
                blob.delete()
            if is_directory_found:
                return {'status': True, 'message': 'Directory [{0}] removed.'.format(directory_full_path)}
            else:
                return {'status': False, 'message': 'Directory [{0}] is not present.'.format(directory_full_path)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to delete directory in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.remove_directory.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def is_file_present(self, directory_full_path, file_name):
        """

        :param directory_full_path:directory_full_path
        :param file_name: Name of file
        :return: {'status': True/False, 'message': 'message detail'}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.list_files(directory_full_path)
            if response['status']:
                if file_name in response['files_list']:
                    return {'status': True, 'message': 'File [{0}] is present.'.format(directory_full_path + file_name)}
            return {'status': False, 'message': 'File [{0}] is not present.'.format(directory_full_path + file_name)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to delete directory in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.is_file_present.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def is_directory_present(self, directory_full_path):
        """

        :param directory_full_path: directory path
        :return: {'status': True/False, 'message': 'message detail"}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.list_directory(directory_full_path)
            if response['status']:
                return {'status': True, 'message': 'Directory [{0}] is present'.format(directory_full_path)}
            return {'status': False, 'message': 'Directory [{0}] is not present'.format(directory_full_path)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to delete directory in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.is_file_present.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def upload_file(self, directory_full_path, file_name, stream_data, local_file_path=False, over_write=False):
        """

        :param directory_full_path: s3 bucket directory
        :param file_name: name you want to specify for file in s3 bucket
        :param local_file_path: your local system file path of file needs to be uploaded
        :param over_write:True if wanted to replace target file if present
        :return:{'status': True/False,
                    'message': 'message detail'}
        """
        try:
            if directory_full_path == "" or directory_full_path == "/":
                directory_full_path = ""
            else:
                if directory_full_path[-1] != "/":
                    directory_full_path += "/"
            response = self.is_directory_present(directory_full_path)
            if not response['status']:
                response = self.create_directory(directory_full_path)
                if not response['status']:
                    return response
            response = self.is_file_present(directory_full_path, file_name)
            if response['status'] and not over_write:
                return {'status': False,
                        'message': 'File [{0}] already present in directory [{1}]. try with overwrite option'.format(
                            file_name, directory_full_path)}

            blob = self.bucket.blob(directory_full_path + file_name)
            if local_file_path:
                blob.upload_from_filename(local_file_path)
            else:
                if isinstance(stream_data,str):
                    stream_data=io.StringIO(stream_data)
                blob.upload_from_file(stream_data)
            return {'status': True,
                    'message': 'File [{0}] uploaded to directory [{1}]'.format(file_name, directory_full_path)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to upload file in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.upload_file.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def download_file(self, directory_full_path, file_name, local_system_directory=False):
        """

        :param directory_full_path:directory_full_path
        :param file_name: Name of file
        :param local_system_directory: file location within your system
        :return: {'status': True/False,
                    'message':'message detail'}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.is_file_present(directory_full_path=directory_full_path, file_name=file_name)
            if local_system_directory:
                local_system_directory = self.update_directory_full_path_string(local_system_directory)
            if not response['status']:
                return response
            blob = self.bucket.blob(directory_full_path + file_name)
            if local_system_directory:
                blob.download_to_filename(local_system_directory+file_name)
                return {'status': True,
                        'message': 'file [{0}] is downloaded in your system at location [{1}] '
                            .format(file_name, local_system_directory)}
            else:
                data = io.BytesIO()
                blob.download_to_file(data)
                return {'status': True,
                        'message': 'file [{0}] is downloaded in your system at location [{1}] '
                            .format(file_name, local_system_directory), 'file_object': data}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to upload file in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.download_file.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def remove_file(self, directory_full_path, file_name):
        """
        :param directory_full_path: provide full directory path along with name
        :param file_name: file name with extension if possible
        :return: {'status': True/False,
                    'message':'message detail'}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.is_file_present(directory_full_path, file_name)
            if response['status']:
                blob = self.bucket.blob(directory_full_path + file_name)
                blob.delete()
                return {'status': True,
                        'message': 'File [{}] deleted from directory [{}]'.format(file_name, directory_full_path)}
            return {'status': False, 'message': response['message']}

        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to remove file in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.remove_file.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def write_file_content(self, directory_full_path, file_name, content, over_write=False):
        """

        :param directory_full_path:  provide full directory path along with name
        :param file_name: file name with extension if possible
        :param content: content need to store in file
        :param over_write:  default False if accept True then overwrite file in directory if exist
        :return: {'status': True/False,
                    'message':'message detail'}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.is_directory_present(directory_full_path)
            if not response['status']:
                response = self.create_directory(directory_full_path)
                if not response['status']:
                    return {'status': False,
                            'message': 'Failed to created directory [{0}] [{1}]'.format(directory_full_path,
                                                                                        response['message'])}
            response = self.is_file_present(directory_full_path, file_name)
            if response['status'] and not over_write:
                return {'status': False,
                        "message": "File [{0}] is already present in directory [{1}]. try with over write option".format(
                            file_name, directory_full_path)}
            blob = self.bucket.blob(directory_full_path + file_name)
            blob.upload_from_file(io.BytesIO(dill.dumps(content)))
            return {'status': True,
                    'message': 'File [{0}] is created in directory [{1}]'.format(file_name, directory_full_path)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create file with content in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.write_file_content.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def update_directory_full_path_string(self, directory_full_path):
        """

        :param directory_full_path: directory_full_path
        :return: update the accepted directory
        """
        try:
            if directory_full_path == "" or directory_full_path == "/":
                directory_full_path = ""
            else:
                if directory_full_path[-1] != "/":
                    directory_full_path = directory_full_path + "/"
            return directory_full_path
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create file with content in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.update_directory_full_path_string.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def read_csv_file(self, directory_full_path, file_name):
        """

        :param directory_full_path: directory_full_path
        :param file_name: file_name
        :return: {'status': True/False,
                    'message': 'message detail',
                    'data_frame': if status True data frame will be returned}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.is_file_present(directory_full_path, file_name)
            if not response['status']:
                return response

            blob = self.bucket.blob(directory_full_path + file_name)
            content=io.BytesIO()
            blob.download_to_file(content)
            content.seek(0)
            df = pd.read_csv(content)
            return {'status': True,
                    'message': 'File [{0}] has been read into data frame'.format(directory_full_path + file_name),
                    'data_frame': df}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create file with content in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.update_directory_full_path_string.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def read_json_file(self,directory_full_path, file_name):
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.is_file_present(directory_full_path, file_name)
            if not response['status']:
                return response
            content = io.BytesIO()
            blob = self.bucket.blob(directory_full_path + file_name)
            blob.download_to_file(content)
            content.seek(0)
            return {'status': True, 'message': 'File [{0}] has been read'.format(directory_full_path + file_name),
                    'file_content': json.loads(content.getvalue())}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create file with content in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.read_json_file.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e


    def read_file_content(self, directory_full_path, file_name):
        """

        :param directory_full_path: directory_full_path
        :param file_name: file_name
        :return: {'status': True/False, 'message': 'message_detail',
                    'file_content':'If status True then Return object which was used to generate the file with write file content'}
        """
        try:
            directory_full_path = self.update_directory_full_path_string(directory_full_path)
            response = self.is_file_present(directory_full_path, file_name)
            if not response['status']:
                return response
            content = io.BytesIO()
            blob=self.bucket.blob(directory_full_path+file_name)
            blob.download_to_file(content)
            content.seek(0)
            return {'status': True, 'message': 'File [{0}] has been read'.format(directory_full_path + file_name),
                    'file_content': dill.loads(content.getvalue())}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create file with content in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.read_file_content.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def move_file(self, source_directory_full_path, target_directory_full_path, file_name, over_write=False,
                  bucket_name=None):
        """

        :param source_directory_full_path: provide source directory path along with name
        :param target_directory_full_path: provide target directory path along with name
        :param file_name: file need to move
        :param over_write:  default False if accept True then overwrite file in target directory if exist
        :return: {'status': True/False,
                        'message': 'message detail'}
        """
        try:
            response = self.copy_file(source_directory_full_path, target_directory_full_path, file_name, over_write,
                                      bucket_name)
            if not response['status']:
                return {'status': False, 'message': 'Failed to move file due to [{}]'.format(response['message'])}
            else:
                if bucket_name is None:
                    bucket_name = self.bucket_name
                self.remove_file(source_directory_full_path, file_name)
                return {'status': True,
                        'message': 'File moved successfully from bucket: [{0}] directory [{1}] to bucket:[{2}] '
                                   'directory[{3}]'.format(self.bucket_name,
                                                           source_directory_full_path + file_name, bucket_name,
                                                           target_directory_full_path + file_name)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create file with content in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.move_file.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e

    def copy_file(self, source_directory_full_path, target_directory_full_path, file_name, over_write=False,
                  bucket_name=None):
        """

        :param source_directory_full_path: provide source directory path along with name
        :param target_directory_full_path: provide target directory path along with name
        :param file_name: file need to copy
        :param over_write: default False if accept True then overwrite file in target directory if exist
        :return: {'status': True/False,
                        'message': 'message detail'}
        """
        try:

            target_directory_full_path = self.update_directory_full_path_string(target_directory_full_path)
            source_directory_full_path = self.update_directory_full_path_string(source_directory_full_path)
            response = self.is_file_present(source_directory_full_path, file_name)
            if not response['status']:
                return {'status': False,
                        'message': 'Source file [{0}] is not present'.format(source_directory_full_path + file_name)}
            if bucket_name is None:
                bucket_name = self.bucket_name
                gcp_obj = self
            else:
                bucket_name = bucket_name
                gcp_obj = GoogleCloudStorage(bucket_name=bucket_name)

            response = gcp_obj.is_file_present(target_directory_full_path, file_name)
            if response['status'] and not over_write:
                return {'status': False,
                        'message': 'Bucket:[{0}] target directory '
                                   '[{1}] contains file [{2}] please'
                                   ' try with over write option.'.format(bucket_name,
                                                                         target_directory_full_path,
                                                                         file_name
                                                                         )}
            response = gcp_obj.is_directory_present(target_directory_full_path)
            if not response['status']:
                response = gcp_obj.create_directory(target_directory_full_path)
                if not response['status']:
                    return {'status': False,
                            'message': 'Failed to created'
                                       ' target directory [{}] in bucket:[{}]'.format(
                                target_directory_full_path,
                                bucket_name
                            )}

            blob=self.bucket.blob(source_directory_full_path+file_name)
            self.bucket.copy_blob(blob,gcp_obj.bucket,target_directory_full_path+file_name)
            return {'status': True,
                    'message': 'File copied successfully from bucket: [{0}] directory [{1}] to bucket:[{2}] '
                               'directory[{3}]'.format(self.bucket_name,
                                                       source_directory_full_path + file_name, bucket_name,
                                                       target_directory_full_path + file_name)}
        except Exception as e:
            google_cloud_exception = GoogleCloudException(
                "Failed to create file with content in module [{0}] class [{1}] method [{2}]"
                    .format(GoogleCloudStorage.__module__.__str__(), GoogleCloudStorage.__name__,
                            self.copy_file.__name__))
            raise Exception(google_cloud_exception.error_message_detail(str(e), sys)) from e
