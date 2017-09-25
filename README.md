memo
<pre>
# 結果の確認
for j in range(len(sentences)):
    data = sentences[j] 
    for i in range(len(data)):
            sys.stdout.write(data[i]['surface'])
    print("\n")
</pre>


<pre>
curl -X POST -H "Content-Type: application/json" -d "{"utt": "hello"}" "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=" -x localhost:yyyy
</pre>
