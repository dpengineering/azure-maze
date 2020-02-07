import numpy as np
from .linalg_helpers import *


class TrackedUser(object):
    def __init__(self, user_id,
                 left_hand, right_hand,
                 torso,
                 left_elbow, right_elbow,
                 left_shoulder, right_shoulder):
        self.user_id = user_id

        self.left_hand = left_hand
        self.right_hand = right_hand

        self.torso = torso

        self.left_elbow = left_elbow
        self.right_elbow = right_elbow

        self.left_shoulder = left_shoulder
        self.right_shoulder = right_shoulder

    @property
    def left_forearm(self):
        return self.left_hand - self.left_elbow

    @property
    def right_forearm(self):
        return self.right_hand - self.right_elbow

    @property
    def left_upper_arm(self):
        return self.left_elbow - self.left_shoulder

    @property
    def right_upper_arm(self):
        return self.right_elbow - self.right_shoulder

    @property
    def left_arm(self):
        return self.left_hand - self.left_shoulder

    @property
    def right_arm(self):
        return self.right_hand - self.right_shoulder


class WorldTrackedUser(TrackedUser):
    def __init__(self, user_id,
                 left_hand, right_hand,
                 torso,
                 left_elbow, right_elbow,
                 left_shoulder, right_shoulder):
        super(WorldTrackedUser, self).__init__(user_id,
                                               left_hand, right_hand,
                                               torso,
                                               left_elbow, right_elbow,
                                               left_shoulder, right_shoulder)
        self._relative_user = None

    def get_forward_plane(self):
        # order of cross is important: ensure that resulting cross product points forward
        return normalize(np.cross(self.get_up_plane(),
                                  self.get_side_plane()))

    def get_up_plane(self):
        # create something that goes vaguely upwards
        vaguely_up = self.right_shoulder - self.torso
        return normalize(project_onto_plane(vaguely_up, self.get_side_plane()))

    def get_side_plane(self):
        return normalize(self.right_shoulder - self.left_shoulder)

    @property
    def relative_user(self):
        if self._relative_user is not None:
            return self._relative_user

        t_matrix = np.linalg.inv((self.get_side_plane(),
                                  self.get_up_plane(),
                                  self.get_forward_plane()))

        lh = np.matmul(t_matrix, self.left_hand - self.torso)
        rh = np.matmul(t_matrix, self.right_hand - self.torso)

        torso = np.matmul(t_matrix, self.torso - self.torso)

        le = np.matmul(t_matrix, self.left_elbow - self.torso)
        re = np.matmul(t_matrix, self.right_elbow - self.torso)

        ls = np.matmul(t_matrix, self.left_shoulder - self.torso)
        rs = np.matmul(t_matrix, self.right_shoulder - self.torso)

        self._relative_user = RelativeTrackedUser(self.user_id,
                                                  lh, rh,
                                                  torso,
                                                  le, re,
                                                  ls, rs,
                                                  self)
        return self._relative_user

class RelativeTrackedUser(TrackedUser):
    def __init__(self, user_id,
                 left_hand, right_hand,
                 torso,
                 left_elbow, right_elbow,
                 left_shoulder, right_shoulder,
                 world_user):
        super(RelativeTrackedUser, self).__init__(user_id,
                                                  left_hand, right_hand,
                                                  torso,
                                                  left_elbow, right_elbow,
                                                  left_shoulder, right_shoulder)
        self.world_user = world_user
