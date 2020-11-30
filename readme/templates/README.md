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

My name is Devon and this is where you can view my public projects. I have a mix of stable and experimental projects, as well as some more comedic repositories.

I work in a handful of different disciplines, but my recent work tends mostly towards reverse engineering, DevOps, and graphical/UX design.

As a fun demonstration of what I can do, this README *dynamically regenerates* using GitHub Actions every hour! (it last updated at **{{ format(now, "%H:%M UTC, %Y-%m-%d") }}**)

<h2>JLPT words of the hour</h2>
<table>
    <tr>
        {%- for level in jlpt_words.keys() %}
        <th>JLPT {{level}}</th>
        {%- endfor %}
    </tr>
    <tr>
        {%- for expression, reading, meaning, tags in jlpt_words.values() %}
        <td>
            <p align="center">{{ reading }}</p>
            <h3 align="center"><b><a href="https://jisho.org/search/{{ quote(expression) }}">{{ expression }}</a></b></h3>
            <hr>
            <p align="center">{{ meaning.replace(';', ';<br>').replace(',', ',<wbr>') | safe}}</p>
        </td>
        {%- endfor %}
    </tr>
</table>

<h2>Other things</h2>
{{ phase_emoji}} Lunar phase
<details>
<summary>{{ hour_emoji }}  World clock inspired by <a href="https://xkcd.com/now">XKCD now</a></summary>

> <img src="generated/now.png" width="512">

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
