import pytest
from os import path, makedirs
import shutil
from shutil import rmtree

from backend.db_cron.setup.logging import logger
from backend.db_cron.utils.misc import (
  repeat_token, 
  invert_dict_list, 
  makedir,
  remove_folder,
  convert_to_bytes,
  update_progress,
)

def test_repeat_token():
  assert repeat_token("abc", 3) == "abcabcabc"
  assert repeat_token("", 2) == ""
  assert repeat_token("x", 0) == ""

def test_invert_dict_list():
  original_dict = {"a": ["b", "c"], "d": ["b", "e"]}
  inverted_dict = invert_dict_list(original_dict)
  assert inverted_dict == {"b": ["a", "d"], "c": ["a"], "e": ["d"]}
  assert invert_dict_list({}) == {}

def test_makedir(mocker):
  # Mock logger.info and logger.warn
  mocker.patch.object(logger, "info")
  mocker.patch.object(logger, "warn")

  # Case 1: Directory doesn't exist
  makedir("new_folder", True)
  assert path.exists("new_folder")
  logger.info.assert_called_once_with('Folder: \n' + repr("new_folder"))

  # Case 2: Directory already exists
  makedir("new_folder", True)
  logger.warn.assert_called_once_with(f'Folder {repr("new_folder")} already exists!')

  # Cleanup
  rmtree("new_folder", ignore_errors=True)

def test_update_progress(capsys):
  update_progress(2, 5, "Downloading files")
  captured = capsys.readouterr()
  assert captured.out == "Downloading files 40.00% 02/05\r"

def test_convert_to_bytes():
  assert convert_to_bytes("10K") == 10240
  assert convert_to_bytes("2.5M") == 2621440
  assert convert_to_bytes("1G") == 1073741824
  
  with pytest.raises(ValueError):
      assert convert_to_bytes("invalid") == None

def test_remove_folder(mocker):
  # Mock logger.error
  mocker.patch.object(logger, "error")

  # Create a temporary folder
  folder_to_remove = "temp_folder"
  makedirs(folder_to_remove)

  remove_folder(folder_to_remove)
  assert not path.exists(folder_to_remove)
  logger.error.assert_not_called()

  # Case 2: Folder doesn't exist
  remove_folder(folder_to_remove)
  error_message="Error deleting folder temp_folder: [Errno 2] No such file or directory: 'temp_folder'"
  logger.error.assert_called_once_with(error_message)

  # Cleanup (already removed in the first call)
  rmtree(folder_to_remove, ignore_errors=True)