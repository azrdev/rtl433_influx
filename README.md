# rtl_433 to InfluxDB

dump everything your rtl-sdr receives on 433MHz into an InfluxDB for easy graphing

## prerequisites

- a systemd linux distro
- python3
- an rtl-sdr and [rtl_433](https://github.com/merbanan/rtl_433)
- InfluxDB and [influxdb-python(3)](https://github.com/influxdata/influxdb-python)

## setup

- setup [rtl_433](https://github.com/merbanan/rtl_433) with your rtl-sdr
    - I assume you use a separate unix user `rtl433sdr` for that, and the compiled binary is (symlinked) in `~rtl433sdr/bin/rtl_433`
- install [InfluxDB](https://github.com/influxdata/influxdb) and [influxdb-python3](https://github.com/influxdata/influxdb-python)
    - create a database `rtl433` where all the stuff goes
- setup the service
~~~sh
cp systemd-tmpfiles.rtl433.conf  /etc/tmpfiles.d/
cp rtl433.service  /etc/systemd/system/
cp rtl433json_to_influx.service  /etc/systemd/system/
systemctl daemon-reload
systemd-tmpfiles --create
systemctl start rtl433 rtl433json_to_influx
systemctl enable rtl433 rtl433json_to_influx
~~~

## graphing

Leave it running overnight, then setup [Grafana](https://github.com/grafana/grafana) and look what you find inside the `rtl433` database!

