# Khan is a unix "top" clone for MongoDB, inspired by Innotop and Motop.

[![Build Status](https://travis-ci.org/globocom/khan.svg?branch=master)](https://travis-ci.org/globocom/khan)

Khan presents a real time list of queries running in a given MongoDB instance and information about the replication status.

## Dependencies

  * Python >= 3.5
  * MongoDB >= 3.0

## Installation


```sh
pip install khan-mongo
```

## Usage

```sh
khan --host <host> [--port <port>] --database <AdminDatabase> -u <user> -p <password> -m [queries|replication]
```

`-m queries` Show current ops

`-m replication` Show replication status/info

## Support

Please [open an issue](https://github.com/globocom/khan/issues) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/globocom/mongo-top/compare/).
