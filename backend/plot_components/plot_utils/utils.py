def get_two_driver_plot_color(driver_1, driver_2, sess):
    driver_1_color = "#" + dict(zip(sess.results.Abbreviation, sess.results.TeamColor))[driver_1]
    driver_2_color = "#" + dict(zip(sess.results.Abbreviation, sess.results.TeamColor))[driver_2]
    if driver_1_color == "#ffffff":
        driver_1_color = "black"
    if driver_2_color == "#ffffff":
        driver_2_color = "black"
    if driver_1_color == driver_2_color:
        driver_1_color = "black"
    return driver_1_color, driver_2_color