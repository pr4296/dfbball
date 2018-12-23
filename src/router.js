import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Players from "@/views/Players.vue"
import Player from "@/views/Player.vue"
import Game from "@/views/Game.vue"
import Team from "@/views/Team.vue"
import Teams from "@/views/Teams.vue"

Vue.use(Router);

export default new Router({
  routes: [
    { path: '/player/:id', component: Player },
    { path: '/teams', component: Teams },
    { path: '/players', component: Players },
    { path: '/team/:id', component: Team },
    { path: '/game/:id', component: Game },
    { path: '/', component: Home }
  ]
});