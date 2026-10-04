export default function TVLayout({children}){

return (

<div className="tv-layout">

<header>

<h1>NSIKAY TV</h1>

<nav>

<a>Live</a>
<a>Replay</a>
<a>Événements</a>
<a>Publicité</a>

</nav>

</header>


<main>

{children}

</main>


</div>

)

}

