sudo umount /var/nfsharefile
#sudo mount -t nfs -o rw,uid=1005,gid=1006 10.192.6.2:/filetrans /var/nfsharefile
sudo mount -t nfs -o rw 10.192.6.2:/filetrans /var/nfsharefile
