from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

# --- データ定義 ---
sandwiches = {
    "ベジーデライト":"ベジ-sb.jpg", "ハム":"ハム-sb.jpg", "たまご":"たまご-sb.jpg", 
    "ツナ":"ツナ-sb.jpg", "アボカドベジー":"アボカド-sb.jpg", "サラダチキン":"サラダチキン-sb.jpg", 
    "チリチキン":"チリチキン-sb.jpg", "BLT":"BLT-sb.jpg", "てり焼きチキン":"てりやき-sb.jpg",
    "えびたま":"えびたま-sb.jpg", "えびアボカド":"えびアボカド-sb.jpg", 
    "生ハム&マスカルポーネ":"生ハムマスカルポーネ-sb.jpg", "アボカドチキン":"アボカドチキン-sb.jpg","てりたま":"てりたま-sb.jpg",
    "アメリカンクラブハウス":"アメリカンクラブハウス-sb.jpg","スパイシークラブハウス":"スパイシークラブハウス-sb.jpg", "ローストビーフ":"ローストビーフ-sb.jpg"
}

toast_options = ["焼く", "焼かない"]
veggie_amounts = ["標準", "抜き", "少なめ", "多め"]

sandwich_ingredients = {
    "ハム":["大豆","豚肉"],"たまご":["卵","乳","大豆","りんご","ゼラチン","アルコール"],"ツナ":["卵","乳","大豆","魚","アルコール"],
    "アボカドベジー":["アルコール"],"サラダチキン":["鶏肉"],"チリチキン":["鶏肉","りんご","アルコール"],"BLT":["ドライソーセージ","乳","大豆","豚肉","鶏肉","アルコール"],
    "てり焼きチキン":["大豆","鶏肉","アルコール"],"えびたま":["えび","卵","大豆","りんご","ゼラチン","アルコール"],"えびアボカド":["えび","アルコール"],
    "生ハム&マスカルポーネ":["生ハム","マスカルポーネ","卵","乳","豚肉"],"アボカドチキン":["鶏肉","アルコール"],"てりたま":["卵","乳","大豆","鶏肉","りんご","ゼラチン","アルコール"],
    "スパイシークラブハウス":["ドライソーセージ","卵","乳","大豆","鶏肉","りんご","ゼラチン","アルコール"],"アメリカンクラブハウス":["卵","大豆","豚肉"],"ローストビーフ":["卵","乳","牛肉","大豆","りんご"]
}

bread_ingredients = {
    "ホワイト":["乳","大豆"],"ウィート":["乳","大豆"],"セサミ":["乳","大豆","ごま"],"ハニーオーツ":["乳","大豆","アルコール"]
}

veggie_ingredients = {
    "レタス":["レタス"], "トマト":["トマト"], "ピーマン":["ピーマン"], "オニオン":["オニオン"], 
    "オリーブ":["オリーブ"],"ピクルス":["ピクルス","アルコール"],"ホットペッパー":["ホットペッパー","アルコール"]
}

topping_ingredients = {
    "ナチュラルチーズ":["ナチュラルチーズ","乳"], "クリームタイプチーズ":["クリームタイプチーズ","乳"], "マスカルポーネチーズ":["マスカルポーネ","乳"], 
    "たまご":["たまご","卵","乳","大豆","りんご","ゼラチン","アルコール"], "ベーコン":["ベーコン","乳","豚肉"],"ツナ":["ツナ","卵","乳","大豆","魚","アルコール"], 
    "えび":["えび"], "アボカド":["アボカド","アルコール"], "ハム":["ハム","豚肉"]
}

sauce_ingredients = {
    "オイル＆ビネガー":["オリーブオイル","ビネガー","アルコール"],"シーザー":["シーザー","卵","乳","大豆","りんご","魚","アルコール"], "野菜クリーミー":["野菜クリーミー","卵","大豆","りんご","アルコール"], 
    "わさび醤油":["わさび醤油","大豆","魚","アルコール"], "チリソース":["チリソース","りんご","アルコール"],"ハニーマスタード":["ハニーマスタード","りんご","アルコール"],
    "バジル":["バジル","大豆","鶏肉"], "チポトレ":["チポトレ","卵","大豆","アルコール"], "マヨ":["マヨ","卵","大豆","アルコール"]
}

@app.route('/')
def index():
    return render_template('index.html', 
                           veggies=veggie_ingredients.keys(), 
                           toppings=topping_ingredients.keys(), 
                           sauces=sauce_ingredients.keys())

@app.route('/gacha', methods=['POST'])
def gacha():
    excluded = request.form.getlist('exclude')
    excluded_set = set(excluded)

    available_sandwiches = [name for name, ing in sandwich_ingredients.items() if not excluded_set & set(ing)]
    available_breads = [name for name, ing in bread_ingredients.items() if not excluded_set & set(ing)]
    filtered_veggies = [name for name, ing in veggie_ingredients.items() if not excluded_set & set(ing)]
    filtered_toppings = [name for name, ing in topping_ingredients.items() if not excluded_set & set(ing)]
    filtered_sauces = [name for name, ing in sauce_ingredients.items() if not excluded_set & set(ing)]

    # --- エラー処理 ---
    if not available_sandwiches or not available_breads:
        error_msg = "条件に合うメニューがありません。除外項目を減らしてください。"
        return render_template('index.html', 
                               error=error_msg,
                               veggies=veggie_ingredients.keys(), 
                               toppings=topping_ingredients.keys(), 
                               sauces=sauce_ingredients.keys())

    # --- 抽選処理 ---
    item_name = random.choice(available_sandwiches)
    item_image = sandwiches[item_name] 

    bread = random.choice(available_breads)
    toast = random.choice(toast_options)

    veggie_custom = {}
    for veg in veggie_ingredients.keys():
        if veg in excluded_set:
            # 除外リストに入っている野菜は、強制的に「抜き」にする
            veggie_custom[veg] = "抜き"
        else:
            # 除外されていない野菜は、通常通りランダムに抽選
            veggie_custom[veg] = random.choice(veggie_amounts)

    add_topping = random.choice([True, False])
    if add_topping and filtered_toppings:
        k_num = min(len(filtered_toppings), random.randint(1, 2))
        topping_choice = random.sample(filtered_toppings, k=k_num)
    else:
        topping_choice = ["なし"]

    if filtered_sauces:
        num_limit = min(len(filtered_sauces), 9)
        num_sauces = random.randint(1, num_limit)
        sauce_choice = random.sample(filtered_sauces, k=num_sauces)
    else:
        sauce_choice = ["なし（全て除外されました）"]

    return render_template('result.html', 
                           item=item_name, 
                           image=item_image, 
                           bread=bread, 
                           toast=toast, 
                           veggies=veggie_custom, 
                           toppings=topping_choice, 
                           sauces=sauce_choice)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)