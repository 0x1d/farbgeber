# farbgeber

A central color generator to provide a uniform colorscheme that is harmonious, yet dynamically changing the color.

Then the color sensor is used in our MQTT network and constantly offers 6 color values. These color values are in harmonious relationship.

This system is intended to serve as an offer for all those who mount LEDs on board our spacestation and eventually face the question how and in what color the LEDs should be lit up. In many cases, this question results in fast fading rainbow "test-patterns" and the rainbow syndrome. The vision is that for each LED installation only blink pattern and light patterns are generated, but the colors come from the color generator.

The color generator is a color Inklusionist and makes sure that all colors of the rainbow are represented equally often and the same length. It produces 6 colors for every second in an hour. Of these 5 colors are very similar and can be used for gradients or backgrounds with movement. The 6th color is in a harmony contrast with the first color and should be used only a little and as a contrast. Rule of thumb: 90-100% of the LEDs should be in one of the 5 basic variations and 0-10% in the contrasting color.

## Example output
```
{
	"c": [206, 71, 235],
	"b": [35, 204, 0],
	"v1": [20, 184, 21],
	"v2": [78, 184, 20],
	"v3": [42, 240, 0],
	"v4": [29, 168, 0]
}
```

## In german

Ein zentraler Farbgeber um der c-base einen farblich einheitlichen und harmonischen, trotzdem dynamisch wechselnden farbton zu verleihen.

Derzeit hat der Farbgeber noch keine MQTT-Anbindung, aber diese soll er in Kürze erhalten. Dann dient der Farbgeber als Sensor in unserem MQTT-Netzwerk und bietet ständig 6 Farbwerte an. Diese Farbwerte stehen in harmonischem Zusammenhang.

Dieses System soll als Angebot dienen für alle diejenigen, die LEDs an Bord verbauen und irgendwann vor der Frage stehen wie und in welcher Farbe die LEDs leuchten sollen. In vielen Fällen resultiert dies in schnellen Regenbogenfading und dem Regenbogensyndrom. Die Vision ist, dass für jede LED-Installation lediglich Blinkmuster und Leuchtpattern erzeugt werden, die Farben aber vom Farbgeber kommen.

Der Farbgeber ist ein Farb-Inklusionist und achtet darauf dass ALLE Farben des Regenbogens gleich oft und gleich lang dargestellt werden. Es werden für jede Sekunde in einer Stunde jeweils 6 Farben erzeugt. Davon sind 5 Farben sich sehr ähnlich und können z.b. für Verläufe oder Hintergründe mit Bewegung genutzt werden. Die 6. Farbe ist der Harmoniekontrast zur ersten Farbe und soll wenig und als hervorstehender Kontrast benutzt werden. Als Faustregel gilt: 90-100% der LEDs sollten in einer der 5 Basisvariationen leuchten und 0-10% in der Kontrastfarbe.


needs: python2

```virtualenv -p /usr/bin/python2.7 venv```

```source venv/bin/activate```

```pip install -r requirements.txt```
