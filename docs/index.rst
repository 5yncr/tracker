.. _index:

5yncr tracker
=============

The tracker consists on one program: ``tracker``.  It takes a listen IP and
port, and will just work from there.  Clients should point to its externally
available IP and port.

The tracker serves as both a DropPeerStore and a PublicKeyStore. The
DropPeerStore provides a way for ``5yncr`` to have access to which
peers have which drops and their respective IP and ports. The
PublicKeyStore provides a way for ``5ycnr`` to have access to the
public keys of peers in the network for purpose of verifing signed metadata
files.

Basic Usage
-----------

To run the tracker a user is going to have to get their externally
addressable IP address, with the required port forwarding. A user could
access this via ``ip a`` or ``ifconfig -a`` with the ethernet or wireless
IP depending on intent. Then run ``python tracker 0.0.0.0 PORT``. Once that is
done users looking to use this tracker can run ``make_tracker_configs IP PORT``
on the ``backend`` side of things where IP is the external IP.

.. autoprogram:: syncr_tracker.tracker:parser()
    :prog: tracker

.. toctree::
    :maxdepth: 1
    :caption: API docs:

    generated/syncr_tracker


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
