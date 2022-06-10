function [errorCode] = XYPVTLoadToMemory(socketId, GroupName, TrajectoryPart)
%XYPVTLoadToMemory :  XY Load PVT trajectory through function
%
%	[errorCode] = XYPVTLoadToMemory(socketId, GroupName, TrajectoryPart)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring TrajectoryPart
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, TrajectoryPart] = calllib('XPS_C8_drivers', 'XYPVTLoadToMemory', socketId, GroupName, TrajectoryPart);
