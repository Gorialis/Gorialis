***

<h1 align="center">
<sub>
    <img src="readme/resources/avatar.png" height="36">
</sub>
&nbsp;
Gorialis
</h1>
<p align="center">
Hello! I like making tangible software.
</p>

***

My name is Devon and this is where you can view my public projects.

I work in a handful of different disciplines, but my recent work tends mostly towards reverse engineering, DevOps, and graphical/UX design.

Provided nothing goes wrong, this README will *dynamically regenerate* using GitHub Actions every hour! (it last updated at **{{ format(now, "%H:%M UTC, %Y-%m-%d") }}**)

<h2>World clock</h2>
<div align="center">
<img align="center" src="generated/now.png" width="512">
</div>

<h2>JLPT words of the hour</h2>
<table align="center">
    {%- for level, (expression, reading, meaning, tags) in jlpt_words.items() %}
    <tr>
        <td>JLPT {{level}}</td>
        <td>
            <p align="center">{{ reading }}</p>
            <h3 align="center"><b><a href="https://jisho.org/search/{{ quote(expression) }}">{{ expression }}</a></b></h3>
        </td>
        <td>
            <p>{{ meaning.replace(';', ';<br>').replace(',', ',<wbr>') | safe}}</p>
        </td>
    </tr>
    {%- endfor %}
</table>

<h2>Other things</h2>
<details>
<summary>{{ phase_emoji }} Lunar phase</summary>

The moon is approximately {{ format(phase * 100, '.2f') }}% through its phase ({{ ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous", "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"][round(phase * 8)] }}).

</details>
<details>
<summary>&#x1f5bc; Fractal of the hour</summary>

> <img src="generated/fractal.png" width="512">

</details>
<details>
<summary>&#x23f2; Year percentage bar</summary>
<pre><code>{{ format(now, '%Y') }} [{{ percentage_bar }}] {{ format(year_percentage * 100, '.2f') }}%</code></pre>
</details>
{{ '' }}
