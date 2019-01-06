import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    apiDataPlayers: [],
    apiDataTeams: [],
    apiDataTeam: {},
    apiDataUpcomingGames: [],
    apiDataCurrentGames: [],
    apiDataRoster: [],
    apiDataTopPlayers: [],
    apiDataPlayerBoxStats: [],
    apiDataDailyTopPlayers: [],
    apiDataGameTopPlayers: [],
    playerCard: [],
    token: [],
    availablePlayerPicks: [],
    picks: [],
    apiDataGamePlayers: [],
  },
  mutations: {
    setApiDataPlayers(state, newApiData) {
        state.apiDataPlayers = newApiData;
    },
    setApiDataTeams(state, newApiData) {
      state.apiDataTeams = newApiData;
    },
    setApiDataTeam(state, newApiData) {
      // console.log(newApiData);
      state.apiDataTeam = newApiData;
    },
    setApiDataUpcomingGames(state, newApiData) {
      state.apiDataUpcomingGames = newApiData;
    },
    setApiDataCurrentGames(state, newApiData) {
      state.apiDataCurrentGames = newApiData;
    },
    setApiDataRoster(state, newApiData) {
      state.apiDataRoster = newApiData;
    },
    setApiDataTopPlayers(state, newApiData) {
      state.apiDataTopPlayers = newApiData;
    },
    setApiDataPlayerBoxStats(state, newApiData) {
      state.apiDataPlayerBoxStats = newApiData;
    },
    setApiDataDailyTopPlayers(state, newApiData) {
      state.apiDataDailyTopPlayers = newApiData;
    },
    setApiDataGameTopPlayers(state, newApiData) {
      state.apiDataGameTopPlayers = newApiData;
    },
    setPlayerCard(state, newApiData) {
      state.playerCard = newApiData;
    },
    setToken(state, newApiData) {
      state.token = newApiData;
    },
    setAvailablePlayerPicks(state, newApiData) {
      state.availablePlayerPicks = newApiData;
    },
    setPicks(state, newApiData) {
      state.picks = newApiData;
    },
    setApiDataGamePlayers(state, newApiData) {
      state.apiDataGamePlayers = newApiData;
    }
  },
  actions: {}
});
