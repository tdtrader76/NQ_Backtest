// ____  __    ___   ________ ___________  ___________ __  ____ ___ 
   // / __ )/ /   /   | / ____/ //_/ ____/   |/_  __<  / // / / __ |__ \
  // / __  / /   / /| |/ /   / ,< / /   / /| | / /  / / // /_/ / / __/ /
 // / /_/ / /___/ ___ / /___/ /| / /___/ ___ |/ /  / /__  __/ /_/ / __/ 
// /_____/_____/_/  |_\____/_/ |_\____/_/  |_/_/  /_/  /_/  \____/____/  

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © blackcat1402
//@version=5
indicator(title='[blackcat] L2 Ehlers Fisherized Deviation Scaled Oscillator', overlay=false, max_labels_count=500)

// Inputs
price = input(hl2, title='Price')
period = input(40, title='Period')
overbought = input(2, title='OverBought')
oversold = input(-2, title='OverSold')

fisherized_deviation_scaled_oscillator(price, period, overbought, oversold) =>
    // Initialize variables
    var a1 = 0.0
    var b1 = 0.0
    var c1 = 0.0
    var c2 = 0.0
    var c3 = 0.0
    var zeros = 0.0
    var filt = 0.0
    var rms = 0.0
    var scaled_filt = 0.0
    var fisher_filt = 0.0
    var trigger = 0.0
    var pi = 2 * math.asin(1)

    // Calculate Super Smoother coefficients
    a1 := math.exp(-1.414 * pi / (0.5 * period))
    b1 := 2 * a1 * math.cos(1.414 * pi / (0.5 * period))
    c2 := b1
    c3 := -a1 * a1
    c1 := 1 - c2 - c3

    // Generate zeros
    zeros := price - nz(price[2])

    // Apply Super Smoother filter
    filt := c1 * (zeros + nz(zeros[1])) / 2 + c2 * nz(filt[1]) + c3 * nz(filt[2])

    // Calculate RMS
    rms := 0
    for count = 0 to period - 1 by 1
        rms += nz(filt[count]) * nz(filt[count])
        rms
    rms := math.sqrt(rms / period)

    // Scale the filter
    scaled_filt := if rms != 0
        filt / rms
    else
        0

    // Apply Fisher Transform
    fisher_filt := if math.abs(scaled_filt) < 2
        0.5 * math.log((1 + scaled_filt / 2) / (1 - scaled_filt / 2))
    else
        0

    // Calculate trigger line
    trigger := 0.05 + 0.9 * nz(fisher_filt[1])

    // Generate alerts
    buy_signal = ta.crossover(fisher_filt, trigger) or ta.crossover(fisher_filt, -1.5) and fisher_filt < 0
    sell_signal = ta.crossunder(fisher_filt, trigger) or ta.crossunder(fisher_filt, 1.5) and fisher_filt > 0

    // Plot labels
    if buy_signal
        label.new(bar_index, fisher_filt[1], 'BUY', color=color.green, textcolor=color.white, style=label.style_label_up, yloc=yloc.price, size=size.small)
    else if sell_signal
        label.new(bar_index, fisher_filt[1], 'SELL', color=color.red, textcolor=color.white, style=label.style_label_down, yloc=yloc.price, size=size.small)

    [fisher_filt, trigger]

// Calculate oscillator
[fisher_filt, trigger] = fisherized_deviation_scaled_oscillator(price, period, overbought, oversold)

// Plot results
p1 = plot(fisher_filt, color=color.new(color.yellow, 0), linewidth=1)
p2 = plot(trigger, color=color.new(color.fuchsia, 0), linewidth=1)
fill(p1, p2, color=fisher_filt > trigger ? color.yellow : color.fuchsia, transp=40)
hline(0)
hline(1.5)
hline(-1.5)

// Add alerts
alertcondition(ta.crossover(fisher_filt, trigger) or ta.crossover(fisher_filt, -1.5) and fisher_filt < 0, title='BUY', message='BUY!')
alertcondition(ta.crossunder(fisher_filt, trigger) or ta.crossunder(fisher_filt, 1.5) and fisher_filt > 0, title='SELL', message='SELL!')

