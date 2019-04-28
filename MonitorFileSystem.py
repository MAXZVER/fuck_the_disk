import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def convert_path_to_unix(path):
    path = path.replace("\\\\", '/')
    path = path.replace("\\", '/')
    return path


def change_path_to_remote(sync_dir, path_file, dir_name):
    list_path_append = []
    current_basename = os.path.basename(path_file)
    while current_basename != dir_name:
        list_path_append.append(current_basename)
        path_file = os.path.dirname(path_file)
        current_basename = os.path.basename(path_file)
    result_path = sync_dir
    for sub_path in reversed(list_path_append):
        result_path = os.path.join(result_path, sub_path)
    return result_path


def get_remote_paths(path_file):
    global monitoring_dir_name
    global sync_dir_linux
    global sync_dir_windows

    remote_paths = {}
    if sync_dir_linux is not None:
        remote_paths["linux"] = change_path_to_remote(sync_dir_linux, path_file, monitoring_dir_name)
    if sync_dir_windows is not None:
        remote_paths["windows"] = change_path_to_remote(sync_dir_windows, path_file, monitoring_dir_name)
    return remote_paths


def not_monitoring_file(path_file):
    global list_not_monitor_file
    if len(list_not_monitor_file) == 0:
        return False
    for file in list_not_monitor_file:
        if file in path_file:
            return True
    return False


def monitoring_file(path_file):
    global list_monitor_file
    if len(list_monitor_file) == 0:
        return True
    for file in list_monitor_file:
        if file in path_file:
            return True
    return False


def monitor_extension(path_file):
    global list_monitor_extension
    if len(list_monitor_extension) == 0:
        return True
    filename, file_extension = os.path.splitext(path_file)
    if file_extension in list_monitor_extension:
        return True
    return False


class MonitorFs(PatternMatchingEventHandler):

    @staticmethod
    def remote_edit(event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        global ssh_transport
        if not monitoring_file(event.src_path) or not_monitoring_file(event.src_path):
            return
        if event.is_directory:
            if event.event_type == "moved":
                ssh_transport.moved_file(event.src_path, event.dest_path)
                return
            if event.event_type == "modified":
                return
            elif event.event_type == "created":
                ssh_transport.mkdir_ssh(event.src_path)
                return
            if event.event_type == "deleted":
                ssh_transport.delete_ssh(event.src_path)
                return
        if not monitor_extension(event.src_path):
            # Check index jetbrains
            if event.event_type == "moved":
                if not monitor_extension(event.dest_path):
                    return
                ssh_transport.copy_remote_file(event.dest_path)
            return
        if event.event_type == "moved":
            if not monitor_extension(event.dest_path):
                return
            ssh_transport.moved_file(event.src_path, event.dest_path)
            return
        if event.event_type == "deleted":
            ssh_transport.delete_ssh(event.src_path)
            return
        if event.event_type == "created" or event.event_type == "modified":
            ssh_transport.copy_remote_file(event.src_path)
        else:
            ssh_transport.copy_remote_file(event.src_path)

    def on_any_event(self, event):
        self.remote_edit(event)