import TVPlayer from "../../components/tv/TVPlayer";
import TVModules from "../../components/tv/TVModules";


export default function TVChannelPage({channel}){


return (

<div>


<h1>{channel.title}</h1>

<p>
{channel.description}
</p>


<TVPlayer />


<TVModules />


</div>

)


}

