**Utilitka pro generovani obrazku iteraci clusterovani**

Utilitka po spusteni spusti cluster program tolikrat, kolik je objektu v input souboru. Pokazde s jinym parametrem N. Scrapuje Smrckovu utilitku pro vizualizaci clusteru od N=max po N=1 a vygenerovana SVG ulozi do HTML souboru. Nasledne se jde pekne v prohlizeci podivat na prubeh generovani clusteru. Useful pro vizuelni overeni, ze algoritmus clusterovani funguje spravne.

**Setup:**

```
pip3 install requests
```

**Usage:**

```
python3 main.py ./cluster input.txt
```

V MACu jde otevrit .html v defaultnim prohlizeci pomoci nasledujiciho commandu. Nevim jak to je jinde.

```
open test_output.html
```


