<script lang="ts">
  import {type DndEvent, dndzone} from "svelte-dnd-action";
  import _ from "lodash";
  import {setDebugMode} from "svelte-dnd-action";
  import {onMount} from "svelte";

  type DraggableItem = {id: string, display: string};

  // let {data}: { data: {champions: string}} = $props();

  let input: string | undefined = $state("");
  let choices = $derived(_.chain(input).split(/\r?\n/).map(line => line.trim()).filter().value());
  let draggableItems: {[id: string]: DraggableItem} = $derived(_.chain(choices).map(value => { return [value, {id: value, display: value}]; }).fromPairs().value());

  let pool: DraggableItem[] = $state([]);
  let teamA: DraggableItem[] = $state([]);
  let teamB: DraggableItem[] = $state([]);

  onMount(async () => {
    input = await (await fetch("/champions.txt")).text()
  })
  // $inspect(pool, teamA, teamB);

  $effect(() => {
      resetPicks();
    }
  );

  function resetPicks() {
    pool = _.values(draggableItems) as DraggableItem[];
    teamA = [];
    teamB = [];
  }

  function handleTeamConsider(team: string, event: CustomEvent<DndEvent<DraggableItem>>): void {
    console.debug("handleTeamConsider", team, event);
    if (team === "A") {
      teamA = _.uniqBy(event.detail.items, i => i.id);
    } else if (team === "B") {
      teamB = _.uniqBy(event.detail.items, i => i.id);
    } else {
      console.log("Invalid team to add item to:", event);
    }
  }

  function handleTeamFinalize(team: string, event: CustomEvent<DndEvent<DraggableItem>>): void {
    console.debug("handleTeamFinalize", team, event);
    if (team === "A") {
      teamA = _.uniqBy(event.detail.items, i => i.id);
    } else if (team === "B") {
      teamB = _.uniqBy(event.detail.items, i => i.id);
    } else {
      console.log("Invalid team to add item to:", event);
    }
  }

  function handleChoicesConsider(event: CustomEvent<DndEvent<DraggableItem>>): void {
    console.debug("CHOICES CONSIDER", event);
    pool = _.uniqBy(event.detail.items, i => i.id);

  }

  function handleChoicesFinalize(event: CustomEvent<DndEvent<DraggableItem>>): void {
    console.debug("CHOICES FINALIZE", event);
    pool = _.uniqBy(event.detail.items, i => i.id);
  }


const dndOptions = {dropTargetStyle: {outline: 'rgba(50, 50, 50, 0.7) dashed 2px'} };
</script>

<div class="grid">
  <div class="header">
    <h1>Nemesis Draft!</h1>
    <h3><i>By Jamie Maclean</i></h3>
  </div>

  <div class="input">
    <span><b>Input:</b></span>
    <span class="subtext">(copy in a list of picks, one per line)</span>
    <textarea bind:value={input}></textarea>

<!--    <button class="start" on:click={resetPicks}>Start!</button>-->

  </div>

  <div class="choices-container">
    <span><b>Choices:</b></span>
    <div class="choices" use:dndzone={{items: pool, ...dndOptions}} on:consider={handleChoicesConsider} on:finalize={handleChoicesFinalize}>
      {#each pool as item(item.id)}
        <div class="item">{item.display}</div>
      {/each}
    </div>
  </div>

  <div class="team-a-container">
    <span><b>Team A:</b></span>
    <div class="team" use:dndzone={{items: teamA, ...dndOptions}} on:consider={(e) => handleTeamConsider("A", e)} on:finalize={(e) => handleTeamFinalize("A", e)}>
      {#each teamA as item(item.id)}
        <div class="item">{item.display}</div>
      {/each}
    </div>
  </div>

  <div class="team-b-container">
    <span><b>Team B:</b></span>
    <div class="team" use:dndzone={{items: teamB, ...dndOptions}} on:consider={(e) => handleTeamConsider("B", e)} on:finalize={(e) => handleTeamFinalize("B", e)}>
      {#each teamB as item(item.id)}
        <div class="item">{item.display}</div>
      {/each}
    </div>
  </div>


</div>

<style>
    :global(body) {
        background: #EEAECA;
        background: linear-gradient(180deg, rgba(238, 174, 202, 0.62) 0%, rgba(148, 187, 233, 0.58) 100%);
        height: 100vh;
        margin: 0;
        padding: 0;
        scrollbar-color: lightcoral transparent;
        scrollbar-width: thin;
    }
    .grid {
        font-size: x-large;
        display: grid;
        grid-template-columns: 40px 1fr 1fr;
        grid-template-rows: 100px 1fr 1fr;
        grid-gap: 1em;
        height: 100%;
        grid-template-areas:
          "header header header"
          "sidebar input choices"
          "sidebar left-team right-team";
    }

    textarea {
        min-width: 200px;
        min-height: 200px;
        width: fit-content;
        font-size: large;
        background-color: transparent;
    }

    .item {
        border: 1px solid black;
        padding: 0.1em 0.5em;
        width: fit-content;
    }

    .team {
        min-width: 200px;
        min-height: 200px;
    }

    .header {
        grid-area: header;
        display: flex;
        flex-direction: column;
        align-items: center;

        h1 {
            margin: 0;
        }
        h3 {
            margin: 0;
            color: #616161;
        }
    }

    .input {
        grid-area: input;
        display: flex;
        flex-direction: column;
        gap: 0.2em;
    }
    .subtext {
        /*margin-left: 0.5em;*/
        font-size: 0.9em;
        color: rgba(50, 50, 50, 0.85);
    }

    .choices-container {
        grid-area: choices;
    }
    .choices {
        display: flex;
        flex-direction: row;
        gap: 0.2em;
        flex-wrap: wrap;
        /*width: 100%;*/
        max-height: 500px;
        overflow-y: scroll;
    }
    .team-a-container {
        grid-area: left-team;
    }
    .team-b-container {
        grid-area: right-team;
    }

    .target-container {
        background-color: blue;
    }

</style>



