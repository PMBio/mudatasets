Multiome datasets
=================

Human PBMCs
-----------

3k PBMCs, granulocytes filtered out:
::
        import mudatasets as mds
	mdata = mds.load("pbmc3k_multiome")


10k PBMCs, granulocytes filtered out:
::
	mdata = mds.load("pbmc10k_multiome")


Human brain cells
-----------------

Human frozen brain:
::
	mdata = mds.load("brain3k_multiome")
