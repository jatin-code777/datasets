
"""`tfds list` command."""

import argparse

# import tensorflow_datasets as tfds
from tensorflow_datasets.core import load


def register_subparser(parsers: argparse._SubParsersAction) -> None:  # pylint: disable=protected-access
  """Add subparser for `new` command."""
  new_parser = parsers.add_parser('list', help='Lists all datasets')
  new_parser.add_argument(
      '--type',  # Optional argument
      type=str,
      help='type of dataset',
  )
  new_parser.set_defaults(subparser_fn=_list_datasets)


def _list_datasets(args: argparse.Namespace) -> None:
  """Creates the dataset directory. Executed by `tfds new <name>`."""
  list_datasets(dataset_type=args.type)


def list_datasets(dataset_type: str):
  if dataset_type:
    datasets = load.list_builders(with_community_datasets=False)
    dataset_type = dataset_type.lower()
    for dataset in datasets:
      section = _get_section(dataset)
      if section == dataset_type:
        print(dataset)
  else:
    list_all_datasets()


def list_all_datasets():
  datasets = load.list_builders(with_community_datasets=False)
  for dataset in datasets:
    print(dataset)


def _get_section(name: str) -> str:
  """Returns the section associated with the dataset."""
  builder_cls = load.builder_cls(name)
  module_parts = builder_cls.__module__.split('.')
  if module_parts[0] != 'tensorflow_datasets':
    raise AssertionError(f'Unexpected dataset {name}: module')
  _, category, *_ = module_parts  # tfds.<category>.xyz
  return category
