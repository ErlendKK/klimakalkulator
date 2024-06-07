import { defineStore } from 'pinia';
import { getData, postData } from '../utils/http-requests.js'
import { getTodaysDate } from '../utils/misc.js'


export const useAuthStore = defineStore('auth', {

  /**
   * Global state
   */
  state: () => ({
    isLoggedIn: false,
    user: null,
    projects: [],
    currentProject: null
  }),
  actions: {

    /**
     * Handle User state
     */
    logIn(user) {
      console.log(user);
      this.isLoggedIn = true;
      this.user = user;
      this.projects = user.projects;
      return true;
    },
    async logOut() {
      await postData({}, '/logout');

      this.isLoggedIn = false;
      this.user = null;
      this.projects = [];
      this.currentProject = null;
    },
    async checkSession() {
      const response = await getData('/session');

      if (response.status === 'success') {
        this.isLoggedIn = true;
        this.user = response;
        this.userName = response.name;
        this.projects = response.projects;

      } else {
        this.isLoggedIn = false;
        this.user = null;
      }
    },

    /**
     * Handle Project state
     */
    setCurrentProject(project) {
      this.currentProject = project;
      console.log('setCurrentProject: ', this.currentProject.name);
      console.log(this.currentProject)
    },
    pushToProjects(project) {
      this.projects.push(project);
    },
    popFromProjects(project_id) {
      console.log(`popFromProjects called for id: ${project_id}`);
      if (this.currentProject?.project_id === project_id) {
        this.currentProject = null;
      }

      this.projects = this.projects.filter(p => p.project_id !== project_id);
    },

    /**
     * Handle Product state
     */
    pushToProducts(product) {
      console.log(`pushToProducts called for id: ${product.product_id}`);
      if (this.currentProject) {
          this.currentProject.products.push(product);
          // updated_product = this.projects?.find(p => p.project_id === currentProject.project_id);
          this.currentProject.updated_date = getTodaysDate();
      }
    },
    popFromProducts(product_id) {
      console.log(`popFromProducts called for id: ${product_id}`);
      if (this.currentProject) {
        this.currentProject.products = this.currentProject.products.filter(p => p.product_id !== product_id);
        this.currentProject.updated_date = getTodaysDate();
      }
    },
  }
});