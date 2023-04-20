import cortex
from cortex import Cortex
import time
import eegControl
import threading

APP_CLIENT_ID = "aIdV6N9RummnH3JlrWFbXlHa5wJp4VO8pCoGhNc0"
APP_CLIENT_SECRET ="lszyfjaAzc3S2YsJJN018RiKuSgFHdCodja6RojyOXEpBInhHs3D8tstmINq14vKOGtkZfA92Sm0FbqgAXAr6SVczPxgxB3rimcVxelNSCUpm5T0iOmDONbGGWA76SeK"
shut_down = False

class BCI_Controller():

    def __init__(self, app_client_id, app_client_secret, **kwargs):
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=True, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(query_profile_done=self.on_query_profile_done)
        self.c.bind(load_unload_profile_done=self.on_load_unload_profile_done)
        self.c.bind(new_com_data=self.on_new_com_data)
        self.c.bind(get_mc_active_action_done=self.on_get_mc_active_action_done)
        self.c.bind(inform_error=self.on_inform_error)


    def start(self, profile_name, headsetId=''):
        """
        To start live process as below workflow
        (1) check access right -> authorize -> connect headset->create session
        (2) query profile -> get current profile -> load/create profile
        (3) get MC active action -> get MC sensitivity -> set new MC sensitivity -> save profile
        (4) subscribe 'com' data to show live MC data
        Parameters
        ----------
        profile_name : string, required
            name of profile
        headsetId: string , optional
             id of wanted headet which you want to work with it.
             If the headsetId is empty, the first headset in list will be set as wanted headset
        Returns
        -------
        None
        """
        if profile_name == '':
            raise ValueError('Empty profile_name. The profile_name cannot be empty.')

        self.profile_name = profile_name
        self.c.set_wanted_profile(profile_name)

        if headsetId != '':
            self.c.set_wanted_headset(headsetId)

        self.c.open()

    def get_active_action(self, profile_name):
        """
        To get active actions for the mental command detection.
        Maximum 4 mental command actions are actived. This doesn't include "neutral"

        Parameters
        ----------
        profile_name : str, required
            profile name

        Returns
        -------
        None
        """

        self.c.get_mental_command_active_action(profile_name)

    def on_create_session_done(self, *args, **kwargs):
        print('on_create_session_done')
        self.c.query_profile()

    def on_query_profile_done(self, *args, **kwargs):
        print('on_query_profile_done')
        self.profile_lists = kwargs.get('data')
        if self.profile_name in self.profile_lists:
            # the profile is existed
            self.c.get_current_profile()
        else:
            # create profile
            print("Creating profile")
            self.c.setup_profile(self.profile_name, 'create')

    def on_load_unload_profile_done(self, *args, **kwargs):
        is_loaded = kwargs.get('isLoaded')
        print("on_load_unload_profile_done: " + str(is_loaded))

        if is_loaded == True:
            # get active action
            stream = ['com']
            self.c.sub_request(stream)
            self.get_active_action(self.profile_name)
            eegControl.intialize()

        else:
            print('The profile ' + self.profile_name + ' is unloaded')
            self.profile_name = ''

    def on_new_com_data(self, *args, **kwargs):
        global shut_down
        """
        To handle mental command data emitted from Cortex

        Returns
        -------
        data: dictionary
             the format such as {'action': 'neutral', 'power': 0.0, 'time': 1590736942.8479}
        """
        if shut_down == False:
            data = kwargs.get('data')
            if data['action'] == 'lift':
                #eegControl.takeOff()
                eegControl.moveForward()
                print("launching")
            elif data['action'] == 'drop':
                #eegControl.land()
                eegControl.moveBackward()
                print("landing")
            elif data['action'] == 'left':
               # eegControl.moveLeft()
                print("Turning left")
            elif data['action'] == 'right':
               # eegControl.moveRight()
                print("Turning right")
            else:
                print('neutral')



       # print('mc data: {}'.format(data))

    def on_get_mc_active_action_done(self, *args, **kwargs):
        data = kwargs.get('data')
        print('on_get_mc_active_action_done: {}'.format(data))
        eegControl.takeOff()
        # self.get_sensitivity(self.profile_name)

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        error_code = error_data['code']
        error_message = error_data['message']

        print(error_data)

        if error_code == cortex.ERR_PROFILE_ACCESS_DENIED:
            # disconnect headset for next use
            print('Get error ' + error_message + ". Disconnect headset to fix this issue for next use.")
            self.c.disconnect_headset()

    def load_profile(self, profile_name):
        """
        To load a profile

        Parameters
        ----------
        profile_name : str, required
            profile name

        Returns
        -------
        None
        """
        self.c.setup_profile(profile_name, 'load')


def landDrone():
    global shut_down
    eegControl.land()
    shut_down = True


def main():
    # Please fill your application clientId and clientSecret before running script

    l = BCI_Controller(APP_CLIENT_ID, APP_CLIENT_SECRET)
    trained_profile_name = 'Ricky'  # Please set a trained profile name here
    time.sleep(5)
    threading.Thread(l.start(trained_profile_name)).start()
    time.sleep(8)
    threading.Thread(eegControl.land()).start()


if __name__ == '__main__':
    main()

