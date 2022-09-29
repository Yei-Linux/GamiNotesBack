## SNIPPETS

In case of problems with instances from replica set , stop MongoDB Service

mongod --port 27017 --dbpath "C:\Program Files\MongoDB\Server\6.0\data\db0" --replSet gami_note_replicaset
mongod --port 27018 --dbpath "C:\Program Files\MongoDB\Server\6.0\data\db1" --replSet gami_note_replicaset
mongod --port 27019 --dbpath "C:\Program Files\MongoDB\Server\6.0\data\db2" --replSet gami_note_replicaset