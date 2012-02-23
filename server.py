#!/usr/bin/env python

import os
import sys
import libtorrent as lt
import time
import urllib

import pymongo


class HandleWrap:

    def __init__(self, handle):
        self.handle = handle

    def peers(self):
        return self.handle.get_peer_info()


class MagnetDaemon:

    def __init__(self):
        self.torrents = []
        self.session = lt.session()
        # self.session.listen_on(8888, 9999)
        self.session.start_dht()
        # self.session.stop_upnp()
        self.session.stop_natpmp()
        self.mongconn = pymongo.Connection()
        self.db = self.mongconn['magnet']
        self.peers = self.db.peers

    def create_handle(self, link=None, path=None):
        params = {
            'save_path': 'tmp',
            # 'upload_mode': True,
            'storage_mode': lt.storage_mode_t.storage_mode_compact,
            'paused': False,
            'auto_managed': True,
        }
        if link:
            return lt.add_magnet_uri(self.session, link, params)
        if path:
            return lt.add_files(self.session, path, params)

    def create_magnet_url(self, info_hash):

        trackers = [
            'http://tracker.openbittorent.org/announce',
            'http://tracker.publicbt.org/announce',
        ]

        s = 'magnet:?xt=urn:btih:%s' % info_hash
        for t in trackers:
            s += '&tr='
            s += urllib.quote(t)
        return s

    def add_from_hash(self, info_hash):
        link = self.create_magnet_url(info_hash)
        handle = self.create_handle(link=link)
        self.add_handle(handle)

    def add_handle(self, handle):
        torrent = HandleWrap(handle)
        self.torrents.append(torrent)
        return torrent

    def add_hashes_from_dump(self, path):
        print 'Reading', path
        for no, line in enumerate(open(path)):
            if no == 50:
                break
            line = line.strip()
            info_hash = self.hash_from_line(line)
            self.add_from_hash(info_hash)

    def hash_from_line(self, line):
        h = line.split('|')
        return h[-1]

    def monitor(self):
        while 1:
            # for torrent in self.torrents:
            #     print torrent.handle.status().distributed_full_copies,
            #     print torrent.handle.status().current_tracker,
            #     print torrent.handle.status().num_seeds,
            #     print torrent.handle.status().list_peers,
            #     print torrent.handle.piece_availability(),
            #     print torrent.handle.has_metadata(),
            #     print

            with_metadata = [t for t in self.torrents if t.handle.has_metadata()]
            for torrent in with_metadata:
                print torrent.handle.name()
                self.add_peers_to_db(torrent)

            print 80 * '-'
            time.sleep(1)

    def add_peers_to_db(self, torrent):
        for p in torrent.peers():
            print " - Client:%s IP:%s Progress:%s" % (p.client, p.ip, p.downloading_total)

            peer = self.peers.find_one({'addr': p.ip})
            if not peer:
                peer = {
                    'addr': p.ip,
                    'torrents': []
                    }

            peer['client'] = p.client
            ih = torrent.info_hash()
            if ih not in peer['torrents']:
                peer['torrents'].append(torrent.handle.info_hash())
            self.peers.save(peer)


def main():
    md = MagnetDaemon()
    md.add_from_hash('2ded86af7c0cce8224262ba703191bf7d8537a5d')
    md.add_from_hash('368a8beaaced1572f44ad5aae0685ed6130d983c')
    md.add_hashes_from_dump('complete')
    md.monitor()

if __name__ == '__main__':
    main()

