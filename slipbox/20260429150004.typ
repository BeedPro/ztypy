#import ".utility/style.typ": style
#show: style

#let title = "TCP Throughput Back-of-the-Envelope"
#let id = 20260429150004

#id:networking:performance:

= #title
Motivated by @01-3.

Approximation:
$ "throughput" approx "cwnd" / "rtt" $.

If congestion window doubles each RTT in slow start, growth is exponential.

= Links
- 20260429150003
- 20260429150006
- 20260429150001

#bibliography(".utility/sources.yaml")
