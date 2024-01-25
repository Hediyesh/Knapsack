from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    n = 1
    W = 10
    v = [10]
    w = [20]

    return render_template('index.html', n=n, W=W, v=v, w=w)


@app.route('/get_result', methods=['POST'])
def get_result():
    print(request.form)
    if request.method == 'POST':
        try:
            # get the parameters
            n = int(request.form.get('n', 1))
            W = float(request.form.get('W', 1))
            v = [float(request.form.get(f'v{i}', 1)) for i in range(1, n+1)]
            w = [float(request.form.get(f'w{i}', 1)) for i in range(1, n+1)]
            # if a number is zero or negative, set it to 1
            for i in range(0, n):
                if v[i] <= 0:
                    v[i] = 1
                if w[i] <= 0:
                    w[i] = 1
            # calculate result and return it
            result_lines, result_val, picked_items, selected_order, selected_percent = max_value(n, v, w, W)

            return jsonify({'result_lines': result_lines, 'result_val': result_val, 'n': n, 'picked_items': picked_items,
                            'selected_order': selected_order, 'selected_percent': selected_percent})
        except Exception as e:
            return jsonify({'error': str(e)})


def max_value(n, v, w, W):
    # define parameters
    selected_order = []
    selected_percent = []
    result_lines = []
    total_value = 0
    # rate of each item
    ratios = [vi / wi for vi, wi in zip(v, w)]
    picked_items = [0] * n
    weight_sum = 0
    c = 1
    while weight_sum < W and c <= n:
        best = 0
        index = 0
        # if the bag still hase space, choose the best one with the best rate
        while index < n:
            if picked_items[index] == 0 and ratios[best] < ratios[index]:
                best = index
            index += 1
        if weight_sum + w[best] <= W:
            # if there is room for 100% of the best item, the best item is added to the bag
            result_lines.append(f"Item ({best + 1}) Has been picked completely")
            selected_percent.append(100)
            total_value += v[best]
            weight_sum += w[best]
            picked_items[best] = 1
            ratios[best] = -1
            selected_order.append(best)
        else:
            # if not, a percent of item is selected and the bag will be full
            picked_items[best] = float(v[best] * (W - weight_sum)) / float(w[best])
            result_lines.append(
                f"Item ({best + 1}) Has been picked with %" + f"{(float(picked_items[best]) / float(v[best]) * 100)}")
            total_value += float(v[best] * (W - weight_sum)) / float(w[best])
            selected_percent.append((float(picked_items[best]) / float(v[best]) * 100))
            weight_sum = W
            selected_order.append(best)
        c += 1
    # return result
    result_val = f"Max value = {total_value}"
    print(picked_items)
    print(selected_order)
    print(selected_percent)
    return result_lines, result_val, picked_items, selected_order, selected_percent


if __name__ == '__main__':
    app.run(debug=True)
