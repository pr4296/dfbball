<template>
  <div class="container">
      <PicksView></PicksView>
      <CurrentGames></CurrentGames>
      <DailyTopPlayers title="Recent Top Players"></DailyTopPlayers>
    </div>
</template>

<script>

import CurrentGames from "@/components/CurrentGames.vue";
import DailyTopPlayers from "@/components/DailyTopPlayers.vue";
import PicksView from "@/components/PicksView.vue";

export default {
  name: "home",
  components: {
    CurrentGames,
    DailyTopPlayers,
    PicksView
  }
};
</script>
