<template>
  <div class="container">
        <MakePicks></MakePicks>
        <CurrentGames></CurrentGames>
        <DailyTopPlayers forteam="all"></DailyTopPlayers>
    </div>
</template>

<script>

import CurrentGames from "@/components/CurrentGames.vue";
import DailyTopPlayers from "@/components/DailyTopPlayers.vue";
import MakePicks from "@/components/MakePicks.vue";

export default {
  name: "home",
  components: {
    CurrentGames,
    DailyTopPlayers,
    MakePicks
  }
};
</script>
