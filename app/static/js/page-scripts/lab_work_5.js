import Vue from "https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.esm.browser.js";

const app = new Vue({
	el: "#input_form",
	data: {
		message: "Hello Vue!",
		x: 2,
		y: 12
	},
	delimiters: ["[[", "]]"]
});
