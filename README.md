# mongo-top - Globo.com Hack Day project

mongo-ops is a unix "top" clone for MongoDB, inspired by Innotop and Motop.

mongo-top presents a real time list of queries running in a given MongoDB  instance and information about the replication status.

## Usage

```sh
mongo-ops --host <host> --port <port> --database <AdminDatabase> -u <user> -p <password> [-p|-r]
```

* -p Show current ops
* -r Show replication status/info

## Dependencies

  * Python >= 3.5
  * MongoDB >= 3.0

## Installation


```sh
pip install mongo-top
```

## Usage

* ToDO

## Support

Please [open an issue](https://github.com/globocom/mongo-top/issues) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/globocom/mongo-top/compare/).
