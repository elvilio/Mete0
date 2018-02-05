#!/usr/bin/env python3
import weather.weather as wd

if __name__ == "__main__":
	loc = [0, 0]
	aaa = wd.Weather('xxxxxxxxxxxxxxxx', loc)

	aaa.create_plot()